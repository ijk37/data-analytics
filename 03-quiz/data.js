// ============================================================================
//  Data Analytics Quiz Data
//  data.js        →  TOPICS list + QUIZ_CONFIG + QUESTIONS scaffold
//  data-01.js ... data-07.js  →  base question pools by chapter
//  data-expansion.js          →  expanded banks and mixed-practice pools
// ============================================================================

const TOPICS = [
  { id: "01", title: "Data & Attribute Types" },
  { id: "02", title: "Descriptive Statistics" },
  { id: "03", title: "Multivariate Analysis" },
  { id: "04", title: "Data Quality & Preprocessing" },
  { id: "05", title: "Clustering" },
  { id: "06", title: "Frequent Pattern Mining" },
  { id: "07", title: "Classification" },
  { id: "mixed-1", title: "Mixed Practice — 50 Questions" },
  { id: "mixed-2", title: "Mixed Practice — 75 Questions" },
  { id: "mixed-3", title: "Mixed Practice — 100 Questions" },
];

const MIXED_IDS = ["mixed-1", "mixed-2", "mixed-3"];

// ── Quiz sizing ─────────────────────────────────────────────────────────────
// Each attempt draws a RANDOM subset of this many questions from the topic
// pool (re-picked on every retry). If a pool is smaller than the configured
// size, the whole pool is used. Override per attempt with a ?n= URL parameter.
const QUIZ_CONFIG = {
  defaultAttempt: 20,
  attempt: {
    "01": 20,
    "02": 25,
    "03": 20,
    "04": 25,
    "05": 20,
    "06": 20,
    "07": 25,
    "mixed-1": 50,
    "mixed-2": 75,
    "mixed-3": 100,
  },
};

// How many questions a given topic shows per attempt (capped at pool size).
function attemptSizeFor(topicId, poolLen) {
  const cfg = (QUIZ_CONFIG.attempt && QUIZ_CONFIG.attempt[topicId]) || QUIZ_CONFIG.defaultAttempt;
  return Math.min(cfg, poolLen);
}

const QUESTIONS = {};
