DROP DATABASE IF EXISTS db;
CREATE DATABASE db;
USE db;

DROP TABLE IF EXISTS challenges;
CREATE TABLE challenges(
	challengeID INTEGER NOT NULL AUTO_INCREMENT,
	challengeName VARCHAR(128) NOT NULL,
	category VARCHAR(128) NOT NULL,
	lastCheck DATETIME NULL,
	lastUp DATETIME NULL,
	status BOOLEAN NULL,
	CONSTRAINT shallenges_pk PRIMARY KEY(challengeID)
);

-- Sample initializer of a challenge in the database

INSERT INTO challenges (challengeName, category)
VALUES ("sampleChallenge", "sampleCategory");


