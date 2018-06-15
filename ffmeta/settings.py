DEBUG = False

# Metadata flatfile location
METADATA_FILE = "data/FFMetadata20180221.csv"

# Database credentials. The following are just placeholders - replace with real credentials.
DB_USER = "user"
DB_PASS = "password"
DB_HOST = "hostname.com"
DB_PORT = 3306
DB_NAME = "dbname"

# SQLAlchemy settings
SQLALCHEMY_DATABASE_URI = "mysql+pymysql://{}:{}@{}:{}/{}?charset=utf8".format(DB_USER, DB_PASS, DB_HOST, DB_PORT, DB_NAME)
SQLALCHEMY_TRACK_MODIFICATIONS = False
