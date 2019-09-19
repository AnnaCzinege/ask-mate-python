DROP TABLE IF EXISTS questions, answers, answer_comments, question_comments, users;

CREATE TABLE questions (
    id SERIAL PRIMARY KEY,
    user_id INT NOT NULL,
    title VARCHAR(255) NOT NULL,
    message VARCHAR(2048) NOT NULL,
    accepted BOOLEAN DEFAULT false
);

CREATE TABLE answers (
    id SERIAL PRIMARY KEY,
    user_id INT NOT NULL,
    question_id INT NOT NULL,
    message VARCHAR(2048) NOT NULL,
    accepted BOOLEAN DEFAULT false
);

CREATE TABLE answer_comments (
    id SERIAL PRIMARY KEY,
    user_id INT NOT NULL,
    answer_id INT NOT NULL,
    comment VARCHAR(2048) NOT NULL
);

CREATE TABLE question_comments (
    id SERIAL PRIMARY KEY,
    user_id INT NOT NULL,
    question_id INT NOT NULL,
    comment VARCHAR(2048) NOT NULL
);

CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username varchar(12) NOT NULL,
    password varchar(500) NOT NULL,
    date date DEFAULT CURRENT_DATE,
    role varchar(20) default 'user'
)
