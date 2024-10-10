from google.cloud.sql.connector import Connector
import sqlalchemy
import pymysql
from utils import *
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
db_conn_name = str(get_env_var("MARKET_DATABASE_CONNECTION_NAME"))
db_zn_username = str(get_env_var("MARKET_DATABASE_ZARA_NEXUS_USERNAME"))
db_zn_password = str(get_env_var("MARKET_DATABASE_ZARA_NEXUS_PASSWORD"))
db_name = str(get_env_var("MARKET_DATABASE_NAME"))

# Set up logging
setup_logging("info")

get_conn(db_conn_name, db_zn_username, db_zn_password, db_name)
logging.info(f"Connected to {db_name} database")

# Create connection pool
pool = sqlalchemy.create_engine(
    "mysql+pymysql://",
    creator=get_conn,
)

# Fetch historical data
data = fetch_historical_data("AAPL", "1d", "1m")

# Print the data
print(data.head())
