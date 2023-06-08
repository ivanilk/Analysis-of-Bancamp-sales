import configparser
from pathlib import Path
config = configparser.ConfigParser()
config.read(Path('./config.ini'))

print(config['GCP']["data_lake_bucket"])