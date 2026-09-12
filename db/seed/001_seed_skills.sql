-- ============================================
-- MASTERYLOOP M1
-- SEED SKILLS
-- ============================================

INSERT INTO skills (name, description)
VALUES
('Python Basics',
 'Introduction to Python programming'),

('Variables',
 'Understanding variables and assignment'),

('Data Types',
 'Understanding Python data types'),

('Operators',
 'Arithmetic, comparison and logical operators'),

('Conditions',
 'Using if, elif and else statements'),

('For Loops',
 'Using for loops for iteration'),

('While Loops',
 'Using while loops for repetition'),

('Lists',
 'Working with Python lists'),

('Dictionaries',
 'Working with Python dictionaries'),

('Functions',
 'Creating and using functions'),

('Parameters',
 'Passing parameters to functions'),

('Return Statements',
 'Returning values from functions');

-- ============================================
-- SKILL PREREQUISITE RELATIONSHIPS
-- ============================================

INSERT INTO skill_edges
(prerequisite_skill_id, skill_id)
VALUES

-- Python Basics → Variables
(1, 2),

-- Variables → Data Types
(2, 3),

-- Data Types → Operators
(3, 4),

-- Operators → Conditions
(4, 5),

-- Conditions → For Loops
(5, 6),

-- Conditions → While Loops
(5, 7),

-- For Loops → Lists
(6, 8),

-- For Loops → Dictionaries
(6, 9),

-- Lists → Functions
(8, 10),

-- Dictionaries → Functions
(9, 10),

-- Functions → Parameters
(10, 11),

-- Parameters → Return Statements
(11, 12); 