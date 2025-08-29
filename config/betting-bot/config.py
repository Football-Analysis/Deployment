import os

class Config:
    MONGO_HOST = os.environ.get("MONGO_HOST", "localhost")
    MOGNO_URL = f"mongodb://{MONGO_HOST}:27017/"

    CERT_LOCATION = os.environ.get("BETFAIR_CERT_DIR", "/home/ubuntu/betfair-cert/")

    DAY_LIMIT = 2

    THRESHOLD = 0.2

    BANKROLL_PERCENTAGE = 0.01
