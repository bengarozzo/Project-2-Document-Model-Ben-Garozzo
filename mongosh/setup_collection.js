// MongoDB shell script: setup collection + indexes for DS 4320 Project 2
// Usage (example):
//   mongosh "YOUR_MONGODB_URI" --file mongosh/setup_collection.js

const DB_NAME = process.env.MONGODB_DB || "ds4320_project2";
const COLLECTION_NAME = process.env.MONGODB_COLLECTION || "clinical_trials";

const dbRef = db.getSiblingDB(DB_NAME);

dbRef.createCollection(COLLECTION_NAME);
const col = dbRef.getCollection(COLLECTION_NAME);

// Primary identifier
col.createIndex({ nct_id: 1 }, { unique: true });

// Common analysis filters / aggregations
col.createIndex({ study_start_year: 1 });
col.createIndex({ phases: 1 });
col.createIndex({ "status.overall_status": 1 });
col.createIndex({ "enrollment.count": 1 });
col.createIndex({ conditions: 1 });
col.createIndex({ "sponsor.lead.class": 1 });
col.createIndex({ "sponsor.lead.name": 1 });
col.createIndex({ "results.has_results": 1 });

print(`Setup complete: ${DB_NAME}.${COLLECTION_NAME}`);

