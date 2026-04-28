"""
clean_trials.py

Reads raw ClinicalTrials.gov documents from MongoDB, cleans them into a
consistent document structure, saves a local JSON copy, and loads the cleaned
documents into a second MongoDB collection.

Input collection:
clinical_trials_project.raw_clinical_trials

Output collection:
clinical_trials_project.clean_clinical_trials
"""

import json
import logging
import os
from pathlib import Path

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

CLEAN_OUTPUT_PATH = DATA_DIR / "clean_clinical_trials_2024_2025.json"
LOG_PATH = LOG_DIR / "pipeline.log"


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

def safe_get(document: dict, *keys):
    """
    Safely access nested dictionary fields.
    Returns None if any key is missing.
    """
    current = document

    for key in keys:
        if not isinstance(current, dict):
            return None
        current = current.get(key)

        if current is None:
            return None

    return current


def clean_interventions(interventions: list) -> list:
    """
    Clean intervention records into a smaller nested structure.
    """
    cleaned = []

    for item in interventions or []:
        cleaned.append({
            "type": item.get("type"),
            "name": item.get("name"),
            "description": item.get("description")
        })

    return cleaned


def clean_arm_groups(arm_groups: list) -> list:
    """
    Clean trial arm/group records.
    """
    cleaned = []

    for item in arm_groups or []:
        cleaned.append({
            "label": item.get("label"),
            "type": item.get("type"),
            "description": item.get("description")
        })

    return cleaned


def clean_outcomes(outcomes: list) -> list:
    """
    Clean outcome records.
    """
    cleaned = []

    for item in outcomes or []:
        cleaned.append({
            "measure": item.get("measure"),
            "description": item.get("description"),
            "time_frame": item.get("timeFrame")
        })

    return cleaned


def clean_trial(raw_trial: dict) -> dict:
    """
    Convert one raw ClinicalTrials.gov document into a cleaner document.
    """
    protocol = raw_trial.get("protocolSection", {})

    identification = protocol.get("identificationModule", {})
    status = protocol.get("statusModule", {})
    sponsor = protocol.get("sponsorCollaboratorsModule", {})
    conditions = protocol.get("conditionsModule", {})
    design = protocol.get("designModule", {})
    arms = protocol.get("armsInterventionsModule", {})
    description = protocol.get("descriptionModule", {})
    outcomes = protocol.get("outcomesModule", {})
    eligibility = protocol.get("eligibilityModule", {})
    oversight = protocol.get("oversightModule", {})

    interventions = clean_interventions(arms.get("interventions", []))
    arm_groups = clean_arm_groups(arms.get("armGroups", []))
    primary_outcomes = clean_outcomes(outcomes.get("primaryOutcomes", []))
    secondary_outcomes = clean_outcomes(outcomes.get("secondaryOutcomes", []))

    cleaned = {
        "nct_id": identification.get("nctId"),
        "brief_title": identification.get("briefTitle"),
        "official_title": identification.get("officialTitle"),
        "source_condition": raw_trial.get("source_condition"),

        "overall_status": status.get("overallStatus"),
        "start_date": safe_get(status, "startDateStruct", "date"),
        "primary_completion_date": safe_get(status, "primaryCompletionDateStruct", "date"),
        "completion_date": safe_get(status, "completionDateStruct", "date"),

        "study_type": design.get("studyType"),
        "phases": design.get("phases", []),
        "enrollment_count": safe_get(design, "enrollmentInfo", "count"),
        "enrollment_type": safe_get(design, "enrollmentInfo", "type"),

        "conditions": conditions.get("conditions", []),
        "keywords": conditions.get("keywords", []),

        "lead_sponsor": safe_get(sponsor, "leadSponsor", "name"),
        "lead_sponsor_class": safe_get(sponsor, "leadSponsor", "class"),

        "brief_summary": description.get("briefSummary"),

        "interventions": interventions,
        "arm_groups": arm_groups,
        "primary_outcomes": primary_outcomes,
        "secondary_outcomes": secondary_outcomes,

        "num_interventions": len(interventions),
        "num_arm_groups": len(arm_groups),
        "num_primary_outcomes": len(primary_outcomes),
        "num_secondary_outcomes": len(secondary_outcomes),
        "num_conditions": len(conditions.get("conditions", [])),

        "healthy_volunteers": eligibility.get("healthyVolunteers"),
        "sex": eligibility.get("sex"),
        "minimum_age": eligibility.get("minimumAge"),

        "is_fda_regulated_drug": oversight.get("isFdaRegulatedDrug"),
        "is_fda_regulated_device": oversight.get("isFdaRegulatedDevice"),

        "has_results": raw_trial.get("hasResults", False)
    }

    return cleaned


# -----------------------------
# Main script
# -----------------------------

def main() -> None:
    """
    Clean raw trial documents and load the cleaned data into MongoDB.
    """
    try:
        load_dotenv(ENV_PATH)
        mongo_uri = os.getenv("MONGO_URI")

        if not mongo_uri:
            raise ValueError("MONGO_URI was not found in .env")

        client = MongoClient(mongo_uri, serverSelectionTimeoutMS=10000)
        client.admin.command("ping")

        db = client["clinical_trials_project"]
        raw_collection = db["raw_clinical_trials"]
        clean_collection = db["clean_clinical_trials"]

        raw_count = raw_collection.count_documents({})
        print(f"Raw documents found: {raw_count}")
        logging.info(f"Raw documents found: {raw_count}")

        if raw_count == 0:
            raise ValueError("No raw documents found in MongoDB")

        cleaned_trials = []

        for raw_trial in raw_collection.find({}):
            cleaned = clean_trial(raw_trial)

            if cleaned.get("nct_id"):
                cleaned_trials.append(cleaned)

        print(f"Clean documents created: {len(cleaned_trials)}")
        logging.info(f"Clean documents created: {len(cleaned_trials)}")

        with open(CLEAN_OUTPUT_PATH, "w", encoding="utf-8") as file:
            json.dump(cleaned_trials, file, indent=2, default=str)

        print(f"Saved cleaned data to: {CLEAN_OUTPUT_PATH}")
        logging.info(f"Saved cleaned data to: {CLEAN_OUTPUT_PATH}")

        clean_collection.delete_many({})
        result = clean_collection.insert_many(cleaned_trials, ordered=False)

        clean_collection.create_index([("nct_id", ASCENDING)], unique=True)
        clean_collection.create_index([("overall_status", ASCENDING)])
        clean_collection.create_index([("source_condition", ASCENDING)])
        clean_collection.create_index([("phases", ASCENDING)])
        clean_collection.create_index([("enrollment_count", ASCENDING)])
        clean_collection.create_index([("lead_sponsor_class", ASCENDING)])

        final_count = clean_collection.count_documents({})

        print("\nClean MongoDB load complete.")
        print(f"Documents inserted: {len(result.inserted_ids)}")
        print(f"Final clean collection count: {final_count}")

        example = clean_collection.find_one(
            {},
            {
                "_id": 0,
                "nct_id": 1,
                "brief_title": 1,
                "overall_status": 1,
                "phases": 1,
                "enrollment_count": 1,
                "source_condition": 1
            }
        )

        print("\nExample clean document:")
        print(example)

        logging.info(f"Final clean collection count: {final_count}")
        logging.info("Clean trial process completed successfully")

    except (PyMongoError, ValueError, json.JSONDecodeError) as error:
        logging.exception("Clean trial pipeline failed")
        print("Clean trial pipeline failed:")
        print(error)

    except Exception as error:
        logging.exception("Unexpected error in clean trial pipeline")
        print("Unexpected error:")
        print(error)


if __name__ == "__main__":
    main()