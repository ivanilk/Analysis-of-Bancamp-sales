from pathlib import Path
import pandas as pd
from prefect import flow, task
from prefect_gcp.cloud_storage import GcsBucket
from prefect_gcp import GcpCredentials
import configparser
from etl_web_to_gcs import etl_web_to_gcs
config = configparser.ConfigParser()
config.read('../config.ini')

@task(retries=3)
def extract_from_gcs(dataset_file: str,) -> Path:
    """Download data from GCS"""
    gcs_path = f"data/{dataset_file}.parquet"
    gcs_block = GcsBucket.load(config['PREFECT']['GcsBucket_block'])
    gcs_block.get_directory(local_path=f"..")
    return Path(f"../{gcs_path}")


@task()
def transform(path: Path) -> pd.DataFrame:
    df = pd.read_parquet(path)
    df["utc_date"] = df['utc_date'] = pd.to_datetime(df['utc_date'].astype(int), unit='s')
    df = df.drop(columns=['track_album_slug_text','amount_over_fmt','item_slug','addl_count'])
    print(df.head(2))
    print(f"columns: {df.dtypes}")
    print(f"rows: {len(df)}")
    return df

@task()
def write_bq(df: pd.DataFrame) -> None:
    """Write DataFrame to BiqQuery"""

    gcp_credentials_block = GcpCredentials.load(config['PREFECT']['GcpCredentials_block'])

    df.to_gbq(
        destination_table=config['GCP']['BQ_DATASET']+'.'+config['GCP']['BQ_TABLE'],
        project_id=config['GCP']['project'],
        credentials=gcp_credentials_block.get_credentials_from_service_account(),
        chunksize=500_000,
        if_exists="append",
    )

@flow()
def etl_gcs_to_bq():
    """Main ETL flow to load data into Big Query"""
    dataset_file = '1000000-bandcamp-sales'
    dataset_url = 'https://www.dropbox.com/s/wd38q80el16i19q/1000000-bandcamp-sales.zip?dl=1'
    etl_web_to_gcs(dataset_url,dataset_file)
    path = extract_from_gcs(dataset_file)
    df = transform(path)
    write_bq(df)

if __name__ == "__main__":
    etl_gcs_to_bq()