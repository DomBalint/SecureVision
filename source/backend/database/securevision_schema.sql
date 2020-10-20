DROP DATABASE IF EXISTS SecureVision;
CREATE DATABASE SecureVision;

USE SecureVision;

DROP TABLE IF EXISTS User;
DROP TABLE IF EXISTS Camera;
DROP TABLE IF EXISTS Image;
DROP TABLE IF EXISTS Detection;
DROP TABLE IF EXISTS Annotation;
DROP TABLE IF EXISTS Feedback;

CREATE TABLE User
(
    id bigint NOT NULL AUTO_INCREMENT,
    name varchar(255) NOT NULL,
    user_pass varchar(255) NOT NULL,
    user_rights int NOT NULL,
    num_feedback int,

    PRIMARY KEY (id)
);


CREATE TABLE Cameras
(
    id bigint NOT NULL AUTO_INCREMENT,
    is_running boolean NOT NULL,

    PRIMARY KEY (id)
);


CREATE TABLE Image
(
    id bigint NOT NULL AUTO_INCREMENT,
    img_path varchar(255) NOT NULL,
    cam_id bigint NOT NULL,


    PRIMARY KEY (id),
    FOREIGN KEY (cam_id) REFERENCES Cameras (id)

);


CREATE TABLE Detection
(
    id bigint NOT NULL AUTO_INCREMENT,
    img_id bigint NOT NULL,

    PRIMARY KEY (id),
    FOREIGN KEY (img_id) REFERENCES Image (id),

);


CREATE TABLE Annotation
(
    id bigint NOT NULL AUTO_INCREMENT,
    obj_type varchar(255) NOT NULL,
    left_x double NOT NULL,
    left_y double NOT NULL,
    length double NOT NULL,
    width double NOT NULL,
    detection_id bigint NOT NULL,

    PRIMARY KEY (id),
    FOREIGN KEY (detection_id) REFERENCES Detection (id)
);

CREATE TABLE Feedback
(
    id bigint NOT NULL AUTO_INCREMENT,
    corr_obj_type varchar(255) NOT NULL,
    corr_left_x double NOT NULL,
    corr_left_y double NOT NULL,
    corr_length double NOT NULL,
    corr_width double NOT NULL,
    detection_id bigint NOT NULL,

    PRIMARY KEY (id),
    FOREIGN KEY (detection_id) REFERENCES Detection (id)
);