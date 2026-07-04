// ============================================================================
//  Data Analytics Quiz Data
//  data.js        →  TOPICS list + QUIZ_CONFIG + QUESTIONS scaffold
//  data-01.js ... data-08.js  →  one starter question pool per chapter
//
//  This is a STARTER pool (~15-20 questions per chapter), not the full
//  ~100-question-per-chapter depth of a mature question bank. Expand any
//  chapter later by pushing more questions onto QUESTIONS["NN"] from a new
//  data-NN-b.js file, loaded after data-NN.js in both index.html and quiz.html.
// ============================================================================

const TOPICS = [
  { id: "01", title: "Data & Attribute Types" },
  { id: "02", title: "Descriptive Statistics" },
  { id: "03", title: "Multivariate Analysis" },
  { id: "04", title: "Data Quality & Preprocessing" },
  { id: "05", title: "Clustering" },
  { id: "06", title: "Frequent Pattern Mining" },
  { id: "07", title: "Classification" },
  { id: "08", title: "Course Summary (Mixed)" },
];

// ── Quiz sizing ─────────────────────────────────────────────────────────────
// Each attempt draws a RANDOM subset of this many questions from the topic
// pool (re-picked on every retry). If a pool is smaller than the configured
// size, the whole pool is used. Override per attempt with a ?n= URL parameter.
const QUIZ_CONFIG = {
  defaultAttempt: 10,   // random questions per attempt (starter pools are smaller than a mature bank)
  attempt: {},          // per-topic overrides — add here once pools grow
};

// How many questions a given topic shows per attempt (capped at pool size).
function attemptSizeFor(topicId, poolLen) {
  const cfg = (QUIZ_CONFIG.attempt && QUIZ_CONFIG.attempt[topicId]) || QUIZ_CONFIG.defaultAttempt;
  return Math.min(cfg, poolLen);
}

const QUESTIONS = {};
