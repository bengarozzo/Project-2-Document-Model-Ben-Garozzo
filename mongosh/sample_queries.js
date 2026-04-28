// MongoDB shell script: sample document-model queries for DS 4320 Project 2
// Usage (example):
//   mongosh "YOUR_MONGODB_URI" --file mongosh/sample_queries.js

const DB_NAME = process.env.MONGODB_DB || "ds4320_project2";
const COLLECTION_NAME = process.env.MONGODB_COLLECTION || "clinical_trials";

const dbRef = db.getSiblingDB(DB_NAME);
const col = dbRef.getCollection(COLLECTION_NAME);

print("=== Sample: count by phase and overall status ===");
col.aggregate([
  { $unwind: { path: "$phases", preserveNullAndEmptyArrays: true } },
  {
    $group: {
      _id: { phase: "$phases", status: "$status.overall_status" },
      n_trials: { $sum: 1 }
    }
  },
  { $sort: { "n_trials": -1 } },
  { $limit: 50 }
]).toArray();

print("=== Sample: enrollment summary by phase (median approx + mean) ===");
col.aggregate([
  { $match: { "enrollment.count": { $type: "number" } } },
  { $unwind: { path: "$phases", preserveNullAndEmptyArrays: false } },
  {
    $group: {
      _id: "$phases",
      n_trials: { $sum: 1 },
      avg_enrollment: { $avg: "$enrollment.count" }
    }
  },
  { $sort: { "n_trials": -1 } }
]).toArray();

print("=== Sample: top conditions ===");
col.aggregate([
  { $unwind: { path: "$conditions", preserveNullAndEmptyArrays: false } },
  { $group: { _id: "$conditions", n_trials: { $sum: 1 } } },
  { $sort: { n_trials: -1 } },
  { $limit: 20 }
]).toArray();

print("=== Sample: sponsor class breakdown ===");
col.aggregate([
  { $group: { _id: "$sponsor.lead.class", n_trials: { $sum: 1 } } },
  { $sort: { n_trials: -1 } }
]).toArray();

print("=== Sample: results posted rate by phase ===");
col.aggregate([
  { $unwind: { path: "$phases", preserveNullAndEmptyArrays: false } },
  {
    $group: {
      _id: "$phases",
      n_trials: { $sum: 1 },
      n_with_results: { $sum: { $cond: ["$results.has_results", 1, 0] } }
    }
  },
  {
    $project: {
      _id: 1,
      n_trials: 1,
      n_with_results: 1,
      pct_with_results: {
        $cond: [
          { $eq: ["$n_trials", 0] },
          null,
          { $multiply: [{ $divide: ["$n_with_results", "$n_trials"] }, 100] }
        ]
      }
    }
  },
  { $sort: { n_trials: -1 } }
]).toArray();

