DROP TABLE IF EXISTS questions, answers, answer_comments, question_comments;

CREATE TABLE questions (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    message VARCHAR(2048) NOT NULL
);

CREATE TABLE answers (
    id SERIAL PRIMARY KEY,
    question_id INT NOT NULL,
    message VARCHAR(2048) NOT NULL
);

CREATE TABLE answer_comments (
    id SERIAL PRIMARY KEY,
    question_id INT NOT NULL,
    comment VARCHAR(2048) NOT NULL
);

CREATE TABLE question_comments (
    id SERIAL PRIMARY KEY,
    question_id INT NOT NULL,
    comment VARCHAR(2048) NOT NULL
);
