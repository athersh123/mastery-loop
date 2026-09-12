
-- ============================================
-- 1. SKILLS
-- ============================================

CREATE TABLE IF NOT EXISTS skills (
    id SERIAL PRIMARY KEY,
    name VARCHAR(200) NOT NULL,
    description TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW()
);


-- ============================================
-- 2. SKILL EDGES
-- Prerequisite relationships between skills
-- ============================================

CREATE TABLE IF NOT EXISTS skill_edges (
    prerequisite_skill_id INTEGER NOT NULL,
    skill_id INTEGER NOT NULL,

    PRIMARY KEY (
        prerequisite_skill_id,
        skill_id
    ),

    FOREIGN KEY (prerequisite_skill_id)
        REFERENCES skills(id),

    FOREIGN KEY (skill_id)
        REFERENCES skills(id),

    CHECK (
        prerequisite_skill_id <> skill_id
    )
);


-- ============================================
-- 3. LEARNERS
-- ============================================

CREATE TABLE IF NOT EXISTS learners (
    id SERIAL PRIMARY KEY,
    external_id VARCHAR(100) UNIQUE,
    display_name VARCHAR(200) NOT NULL,
    cohort VARCHAR(100),
    created_at TIMESTAMPTZ DEFAULT NOW()
);


-- ============================================
-- 4. CLASSES
-- ============================================

CREATE TABLE IF NOT EXISTS classes (
    id SERIAL PRIMARY KEY,
    name VARCHAR(200) NOT NULL,
    description TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW()
);


-- ============================================
-- 5. ENROLLMENTS
-- Connects learners with classes
-- ============================================

CREATE TABLE IF NOT EXISTS enrollments (
    learner_id INTEGER NOT NULL,
    class_id INTEGER NOT NULL,

    PRIMARY KEY (
        learner_id,
        class_id
    ),

    FOREIGN KEY (learner_id)
        REFERENCES learners(id),

    FOREIGN KEY (class_id)
        REFERENCES classes(id)
);


-- ============================================
-- 6. ITEM BANK
-- Questions
-- ============================================

CREATE TABLE IF NOT EXISTS items (
    id SERIAL PRIMARY KEY,

    stem_md TEXT NOT NULL,

    options JSONB NOT NULL,

    answer_key TEXT NOT NULL,

    rationale_md TEXT,

    skill_ids INTEGER[] NOT NULL,

    state VARCHAR(50) DEFAULT 'draft',

    origin VARCHAR(50) DEFAULT 'human',

    lineage JSONB,

    difficulty DOUBLE PRECISION,

    discrimination DOUBLE PRECISION,

    exposure_count INTEGER DEFAULT 0,

    created_at TIMESTAMPTZ DEFAULT NOW(),

    updated_at TIMESTAMPTZ DEFAULT NOW()
);


-- ============================================
-- 7. INTERACTIONS
-- APPEND-ONLY LEARNER RESPONSE STORE
-- ============================================

CREATE TABLE IF NOT EXISTS interactions (
    id BIGSERIAL PRIMARY KEY,

    learner_id INTEGER NOT NULL,

    item_id INTEGER NOT NULL,

    session_id VARCHAR(100),

    shown_at TIMESTAMPTZ,

    responded_at TIMESTAMPTZ,

    response TEXT,

    correct BOOLEAN,

    latency_ms INTEGER,

    scored BOOLEAN DEFAULT TRUE,

    pilot BOOLEAN DEFAULT FALSE,

    created_at TIMESTAMPTZ DEFAULT NOW(),

    FOREIGN KEY (learner_id)
        REFERENCES learners(id),

    FOREIGN KEY (item_id)
        REFERENCES items(id)
);


-- ============================================
-- INDEXES
-- ============================================

CREATE INDEX IF NOT EXISTS idx_interactions_learner
ON interactions(learner_id);

CREATE INDEX IF NOT EXISTS idx_interactions_item
ON interactions(item_id);

CREATE INDEX IF NOT EXISTS idx_interactions_created
ON interactions(created_at);

CREATE INDEX IF NOT EXISTS idx_items_state
ON items(state);

CREATE INDEX IF NOT EXISTS idx_learners_external
ON learners(external_id);