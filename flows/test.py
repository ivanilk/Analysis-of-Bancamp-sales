import configparser
import Path
config = configparser.ConfigParser()
config.read(Path('../config.ini'))

print(config)