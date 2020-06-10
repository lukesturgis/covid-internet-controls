CREATE DATABASE IF NOT EXISTS covid_internet_controls;
USE covid_internet_controls;

CREATE TABLE IF NOT EXISTS countries (
    country_code VARCHAR(2) NOT NULL,
    country_name VARCHAR(64) NOT NULL,
    continent VARCHAR(64),
    PRIMARY KEY (country_code)
);

CREATE TABLE IF NOT EXISTS workers (
    worker_ip VARCHAR(32) NOT NULL,
    country_code VARCHAR(2) NOT NULL,
    city VARCHAR(256),
    PRIMARY KEY (worker_ip), 
    FOREIGN KEY (country_code) REFERENCES countries(country_code)
);

CREATE TABLE IF NOT EXISTS response (
    id INT NOT NULL AUTO_INCREMENT,
    success BOOLEAN NOT NULL,
    status_code INT NOT NULL,
    content LONGBLOB NOT NULL,
    content_hash CHAR(32) NOT NULL,
    PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS request (
    id INT NOT NULL AUTO_INCREMENT,
    worker_ip VARCHAR(32) NOT NULL, 
    domain VARCHAR(256) NOT NULL,
    path VARCHAR(256) NOT NULL,
    response_id INT NOT NULL,
    protocol VARCHAR(5) NOT NULL,
    PRIMARY KEY (id),
    FOREIGN KEY (worker_ip) REFERENCES workers(worker_ip),
    FOREIGN KEY (response_id) REFERENCES response(id)
);

