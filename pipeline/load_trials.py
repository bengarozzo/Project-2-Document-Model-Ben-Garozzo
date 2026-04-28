"""
load_trials.py

Pulls raw clinical trial records from ClinicalTrials.gov and loads them
into MongoDB Atlas.

This script:
1. Pulls interventional drug trials from 2024-2025
2. Uses balanced condition groups
3. Saves raw JSON locally
4. Loads raw documents into MongoDB
5. Adds indexes
6. Logs progress and errors
"""

import json
import logging
import os
from pathlib import Path

import requests
from dotenv import load_dotenv
from pymongo import MongoClient, ASCENDING
from pymongo.errors import PyMongoError


# -----------------------------
# Paths and constants
# -----------------------------

ROOT_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT_DIR / "data"
LOG_DIR = ROOT_DIR / "logs"
ENV_PATH = ROOT_DIR / ".env"

DATA_DIR.mkdir(exist_ok=True)
LOG_DIR.mkdir(exist_ok=True)

RAW_OUTPUT_PATH = DATA_DIR / "raw_clinical_trials_2024_2025.json"
LOG_PATH = LOG_DIR / "pipeline.log"

BASE_URL = "https://clinicaltrials.gov/api/v2/studies"

CONDITIONS = ["cancer", "diabetes", "heart disease"]
MAX_RECORDS_PER_CONDITION = 500


# -----------------------------
# Logging setup
# -----------------------------

logging.basicConfig(
    filename=LOG_PATH,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


# -----------------------------
# Helper functions
# -----------------------------

def fetch_trials_for_condition(condition: str, max_records: int = 500) -> list[dict]:
    """
    Pull clinical trial records for one condition from ClinicalTrials.gov.

    The function stops after max_records so one condition does not dominate
    the dataset.
    """
    trials = []
    next_page_token = None

    try:
        while len(trials) < max_records:
            params = {
                "query.cond": condition,
                "filter.advanced": (
                    "AREA[StudyType]INTERVENTIONAL "
                    "AND AREA[InterventionType]DRUG "
                    "AND AREA[StartDate]RANGE[2024-01-01,2025-12-31]"
                ),
                "pageSize": 100,
                "format": "json",
            }

            if next_page_token:
                params["pageToken"] = next_page_token

            response = requests.get(BASE_URL, params=params, timeout=30)
            response.raise_for_status()

            data = response.json()
            batch = data.get("studies", [])

            for trial in batch:
                trial["source_condition"] = condition

            trials.extend(batch)

            print(f"{condition}: pulled {len(batch)} this batch, {len(trials)} total")
            logging.info(f"{condition}: pulled {len(batch)} this batch, {len(trials)} total")

            next_page_token = data.get("nextPageToken")

            if not next_page_token or len(batch) == 0:
                break

        return trials[:max_records]

    except requests.RequestException as error:
        logging.exception(f"API request failed for condition: {condition}")
        print(f"API request failed for {condition}: {error}")
        return []


def get_nct_id(trial: dict) -> str | None:
    """
    Extract NCT ID from a raw ClinicalTrials.gov record.
    """
    return (
        trial.get("protocolSection", {})
        .get("identificationModule", {})
        .get("nctId")
    )


def deduplicate_trials(trials: list[dict]) -> list[dict]:
    """
    Remove duplicate trials using NCT ID.
    """
    unique_trials = {}

    for trial in trials:
        nct_id = get_nct_id(trial)

        if nct_id:
            unique_trials[nct_id] = trial

    return list(unique_trials.values())


def load_to_mongo(trials: list[dict]) -> None:
    """
    Load raw clinical trial documents into MongoDB Atlas.
    """
    load_dotenv(ENV_PATH)
    mongo_uri = os.getenv("MONGO_URI")

    if not mongo_uri:
        raise ValueError("MONGO_URI was not found in .env")

    client = MongoClient(mongo_uri, serverSelectionTimeoutMS=10000)
    client.admin.command("ping")

    print("Connected to MongoDB")
    logging.info("Connected to MongoDB")

    db = client["clinical_trials_project"]
    collection = db["raw_clinical_trials"]

    deleted = collection.delete_many({})
    logging.info(f"Deleted {deleted.deleted_count} existing raw documents")

    if len(trials) == 0:
        raise ValueError("No trials available to load into MongoDB")

    result = collection.insert_many(trials, ordered=False)
    inserted_count = len(result.inserted_ids)

    collection.create_index(
        [("protocolSection.identificationModule.nctId", ASCENDING)],
        unique=True
    )
    collection.create_index([("source_condition", ASCENDING)])
    collection.create_index([("protocolSection.statusModule.overallStatus", ASCENDING)])
    collection.create_index([("protocolSection.designModule.phases", ASCENDING)])

    final_count = collection.count_documents({})

    print("\nRaw MongoDB load complete.")
    print(f"Documents inserted: {inserted_count}")
    print(f"Final collection count: {final_count}")

    logging.info(f"Inserted {inserted_count} raw documents")
    logging.info(f"Final raw collection count: {final_count}")


# -----------------------------
# Main script
# -----------------------------

def main() -> None:
    """
    Pull balanced clinical trial records and load them into MongoDB.
    """
    try:
        logging.info("Starting clinical trial pull and load process")

        all_trials = []

        for condition in CONDITIONS:
            trials = fetch_trials_for_condition(
                condition,
                max_records=MAX_RECORDS_PER_CONDITION
            )
            all_trials.extend(trials)

        print(f"\nTotal pulled before deduplication: {len(all_trials)}")
        logging.info(f"Total pulled before deduplication: {len(all_trials)}")

        unique_trials = deduplicate_trials(all_trials)

        print(f"Total unique trials after deduplication: {len(unique_trials)}")
        logging.info(f"Total unique trials after deduplication: {len(unique_trials)}")

        with open(RAW_OUTPUT_PATH, "w", encoding="utf-8") as file:
            json.dump(unique_trials, file, indent=2)

        print(f"Saved raw data to: {RAW_OUTPUT_PATH}")
        logging.info(f"Saved raw data to: {RAW_OUTPUT_PATH}")

        load_to_mongo(unique_trials)

        logging.info("Clinical trial pull and load process completed successfully")

    except (ValueError, PyMongoError, json.JSONDecodeError) as error:
        logging.exception("Pipeline failed")
        print("Pipeline failed:")
        print(error)

    except Exception as error:
        logging.exception("Unexpected error")
        print("Unexpected error:")
        print(error)


if __name__ == "__main__":
    main()