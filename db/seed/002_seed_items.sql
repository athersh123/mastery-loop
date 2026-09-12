-- ============================================
-- MASTERYLOOP M1
-- SEED ITEM BANK
-- ============================================


-- Q1: Python Basics

INSERT INTO items (
    stem_md,
    options,
    answer_key,
    rationale_md,
    skill_ids,
    state,
    origin,
    difficulty
)
VALUES (
    'Which programming language are we using in this course?',
    '{"A":"Java","B":"Python","C":"C++","D":"Ruby"}',
    'B',
    'Python is the programming language used in this curriculum.',
    ARRAY[1],
    'active',
    'human',
    0.2
);


-- Q2: Variables

INSERT INTO items (
    stem_md,
    options,
    answer_key,
    rationale_md,
    skill_ids,
    state,
    origin,
    difficulty
)
VALUES (
    'Which symbol is used for assignment in Python?',
    '{"A":"==","B":"=","C":"!=","D":">="}',
    'B',
    'The single equal sign is used to assign a value to a variable.',
    ARRAY[2],
    'active',
    'human',
    0.2
);


-- Q3: Data Types

INSERT INTO items (
    stem_md,
    options,
    answer_key,
    rationale_md,
    skill_ids,
    state,
    origin,
    difficulty
)
VALUES (
    'Which data type is used to store True or False?',
    '{"A":"int","B":"float","C":"bool","D":"str"}',
    'C',
    'The bool data type represents True or False values.',
    ARRAY[3],
    'active',
    'human',
    0.2
);


-- Q4: Operators

INSERT INTO items (
    stem_md,
    options,
    answer_key,
    rationale_md,
    skill_ids,
    state,
    origin,
    difficulty
)
VALUES (
    'Which operator is used for addition in Python?',
    '{"A":"+","B":"-","C":"*","D":"/"}',
    'A',
    'The + operator performs addition.',
    ARRAY[4],
    'active',
    'human',
    0.2
);


-- Q5: Conditions

INSERT INTO items (
    stem_md,
    options,
    answer_key,
    rationale_md,
    skill_ids,
    state,
    origin,
    difficulty
)
VALUES (
    'Which keyword is used to create a condition in Python?',
    '{"A":"if","B":"loop","C":"check","D":"condition"}',
    'A',
    'The if keyword is used to execute code based on a condition.',
    ARRAY[5],
    'active',
    'human',
    0.2
);


-- Q6: For Loops

INSERT INTO items (
    stem_md,
    options,
    answer_key,
    rationale_md,
    skill_ids,
    state,
    origin,
    difficulty
)
VALUES (
    'Which loop is commonly used to iterate over a list?',
    '{"A":"if","B":"for","C":"try","D":"def"}',
    'B',
    'A for loop can iterate through each element of a list.',
    ARRAY[6],
    'active',
    'human',
    0.2
);


-- Q7: While Loops

INSERT INTO items (
    stem_md,
    options,
    answer_key,
    rationale_md,
    skill_ids,
    state,
    origin,
    difficulty
)
VALUES (
    'Which keyword starts a while loop in Python?',
    '{"A":"repeat","B":"while","C":"loop","D":"during"}',
    'B',
    'The while keyword starts a while loop.',
    ARRAY[7],
    'active',
    'human',
    0.2
);


-- Q8: Lists

INSERT INTO items (
    stem_md,
    options,
    answer_key,
    rationale_md,
    skill_ids,
    state,
    origin,
    difficulty
)
VALUES (
    'Which brackets are used to create a Python list?',
    '{"A":"()","B":"{}","C":"[]","D":"<>"}',
    'C',
    'Square brackets are used to create a Python list.',
    ARRAY[8],
    'active',
    'human',
    0.2
);


-- Q9: Dictionaries

INSERT INTO items (
    stem_md,
    options,
    answer_key,
    rationale_md,
    skill_ids,
    state,
    origin,
    difficulty
)
VALUES (
    'Which data structure stores data as key-value pairs in Python?',
    '{"A":"List","B":"Tuple","C":"Dictionary","D":"Set"}',
    'C',
    'A Python dictionary stores data as key-value pairs.',
    ARRAY[9],
    'active',
    'human',
    0.2
);


-- Q10: Functions

INSERT INTO items (
    stem_md,
    options,
    answer_key,
    rationale_md,
    skill_ids,
    state,
    origin,
    difficulty
)
VALUES (
    'Which keyword is used to define a function in Python?',
    '{"A":"function","B":"define","C":"def","D":"fun"}',
    'C',
    'The def keyword is used to define a function in Python.',
    ARRAY[10],
    'active',
    'human',
    0.2
);


-- Q11: Parameters

INSERT INTO items (
    stem_md,
    options,
    answer_key,
    rationale_md,
    skill_ids,
    state,
    origin,
    difficulty
)
VALUES (
    'What is a parameter in a Python function?',
    '{"A":"A value passed to a function","B":"A loop","C":"A data type","D":"A comment"}',
    'A',
    'A parameter is a variable that receives a value when the function is called.',
    ARRAY[11],
    'active',
    'human',
    0.2
);


-- Q12: Return Statements

INSERT INTO items (
    stem_md,
    options,
    answer_key,
    rationale_md,
    skill_ids,
    state,
    origin,
    difficulty
)
VALUES (
    'Which keyword sends a value back from a Python function?',
    '{"A":"send","B":"return","C":"back","D":"output"}',
    'B',
    'The return keyword sends a value back from a function.',
    ARRAY[12],
    'active',
    'human',
    0.2
);