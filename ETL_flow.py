from pathlib import Path
import pandas as pd
from prefect import flow, task
from prefect_gcp.cloud_storage import GcsBucket
from random import randint
from prefect.tasks import task_input_hash
from datetime import timedelta


#task(retries=3, cache_key_fn=task_input_hash, cache_expiration=timedelta(days=1))
@task(retries=3)
def fetch(dataset_url: str) -> pd.DataFrame:
    df = pd.read_csv(dataset_url)
    return df


@task(log_prints=True)
def clean(df: pd.DataFrame) -> pd.DataFrame:
    """Fix dtype issues"""
    df["utc_date"] = df['utc_date'] = pd.to_datetime(df['utc_date'].astype(int), unit='s')
    df = df.drop(columns=['track_album_slug_text','amount_over_fmt','item_slug','addl_count'])
    print(df.head(2))
    print(f"columns: {df.dtypes}")
    print(f"rows: {len(df)}")
    return df


@task()
def write_local(df: pd.DataFrame, dataset_file: str) -> Path:
    """Write DataFrame out as parquet file"""
    data_dir = f'../data'
    Path(data_dir).mkdir(parents=True, exist_ok=True)
    path = Path(f'{data_dir}/{dataset_file}.parquet')
    df.to_parquet(path, compression='gzip')
    return path


@task()
def write_gcs(path: Path) -> None:
    """Upload local parquet file to GCS"""
    gcp_cloud_storage_bucket_block = GcsBucket.load("zoom-gcs")
    gcp_cloud_storage_bucket_block.upload_from_path(from_path=path, to_path=f"{path}".replace("\\","/").removeprefix("../"), timeout=9000)
    return


@flow()
def etl_web_to_gcs() -> None:
    """The main ETL function"""
    dataset_file = 'data_cleaned'
    dataset_url = './data/1000000-bandcamp-sales.csv'

    df = fetch(dataset_url)
    df_clean = clean(df)
    path = write_local(df_clean, dataset_file)
    write_gcs(path)

if __name__ == "__main__":
    etl_web_to_gcs()