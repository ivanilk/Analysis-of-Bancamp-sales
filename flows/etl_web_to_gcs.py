from pathlib import Path
import pandas as pd
from prefect import flow, task
from prefect_gcp.cloud_storage import GcsBucket
from random import randint
from prefect.tasks import task_input_hash
from datetime import timedelta
import configparser
import wget
import os
config = configparser.ConfigParser()
config.read('../config.ini')

#task(retries=3, cache_key_fn=task_input_hash, cache_expiration=timedelta(days=1))
@task(retries=3)
def fetch(dataset_url: str) -> pd.DataFrame:
    out = dataset_url.split('/')[-1].replace('?dl=1','')
    filename=f"../data/{out}"
    if os.path.exists(filename):
        os.remove(filename) 
    wget.download(dataset_url, out=filename)
    df = pd.read_csv(filename)
    return df


@task()
def write_gcs(df: pd.DataFrame,dataset_file:str) -> None:
    """Upload local parquet file to GCS"""
    gcp_cloud_storage_bucket_block = GcsBucket.load(config['PREFECT']['GcsBucket_block'])
    gcp_cloud_storage_bucket_block.upload_from_dataframe(df=df, to_path=f"./data/{dataset_file}.parquet",serialization_format='parquet',timeout=9000)
    return


@flow()
def etl_web_to_gcs(dataset_url,dataset_file) -> None:
    """The main ETL function"""
    df = fetch(dataset_url)
    write_gcs(df,dataset_file)

if __name__ == "__main__":
    etl_web_to_gcs()