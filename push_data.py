import os
import sys
import json
from pathlib import Path

import certifi
import pandas as pd
import pymongo
from dotenv import load_dotenv

from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
from networksecurity.constant.training_pipeline import (
    DATA_INGESTION_DATABASE_NAME,
    DATA_INGESTION_COLLECTION_NAME,
)

# Load environment variables
load_dotenv()

MONGO_DB_URL = os.getenv("MONGO_DB_URL")
CA_CERTIFICATE_PATH = certifi.where()


class NetworkDataExtract:

    def csv_to_json_convertor(self, file_path: str) -> list:
        try:
            data = pd.read_csv(file_path)

            # Convert CSV records into a list of dictionaries
            records = json.loads(data.to_json(orient="records"))

            logging.info(f"Converted {len(records)} CSV records to JSON")
            return records

        except Exception as e:
            raise NetworkSecurityException(e, sys) from e

    def insert_data_mongodb(
        self, records: list, database: str, collection: str
    ) -> int:
        try:
            if not MONGO_DB_URL:
                raise ValueError(
                    "MONGO_DB_URL is missing from the .env file"
                )

            if not records:
                raise ValueError("No records available to insert")

            # Connect to MongoDB Atlas
            with pymongo.MongoClient(
                MONGO_DB_URL,
                tlsCAFile=CA_CERTIFICATE_PATH,
            ) as mongo_client:

                mongo_client.admin.command("ping")

                db = mongo_client[database]
                collection_obj = db[collection]

                result = collection_obj.insert_many(records)

                inserted_count = len(result.inserted_ids)

                logging.info(
                    f"Successfully inserted {inserted_count} records "
                    f"into {database}.{collection}"
                )

                return inserted_count

        except Exception as e:
            raise NetworkSecurityException(e, sys) from e


if __name__ == "__main__":
    try:
        # Build the CSV path relative to this script
        FILE_PATH = (
            Path(__file__).resolve().parent
            / "Network_Data"
            / "phisingData.csv"
        )

        # Use the same database and collection as Data Ingestion
        DATABASE = DATA_INGESTION_DATABASE_NAME
        COLLECTION = DATA_INGESTION_COLLECTION_NAME

        network_obj = NetworkDataExtract()

        records = network_obj.csv_to_json_convertor(
            file_path=str(FILE_PATH)
        )

        print(f"Records read from CSV: {len(records)}")

        no_of_records = network_obj.insert_data_mongodb(
            records,
            DATABASE,
            COLLECTION,
        )

        print(f"Records inserted into MongoDB: {no_of_records}")

    except Exception as e:
        raise NetworkSecurityException(e, sys) from e