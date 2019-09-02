DROP TABLE IF EXISTS questions, answers, comment_table;

CREATE TABLE questions (
   id SERIAL PRIMARY KEY,
   title VARCHAR(255) NOT NULL,
   message VARCHAR(2048) NOT NULL
);

CREATE TABLE answers (
    id SERIAL PRIMARY KEY,
    question_id int NOT NULL,
    message VARCHAR(2048) NOT NULL
);

CREATE TABLE comment_table (
    id SERIAL PRIMARY KEY,
    question_id int NOT NULL,
    comment VARCHAR(2048) NOT NULL
);