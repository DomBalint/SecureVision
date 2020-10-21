CREATE TABLE user (
	id INTEGER NOT NULL,
	name VARCHAR(100),
	user_pass VARCHAR(50),
	user_rights INTEGER,
	num_feedback INTEGER,
	PRIMARY KEY (id)
);


CREATE TABLE camera (
	id INTEGER NOT NULL,
	is_running BOOLEAN,
	PRIMARY KEY (id),
	CHECK (is_running IN (0, 1))
);


CREATE TABLE image (
	id INTEGER NOT NULL,
	img_path VARCHAR(200),
	cam_id INTEGER,
	PRIMARY KEY (id),
	FOREIGN KEY(cam_id) REFERENCES camera (id)
);


CREATE TABLE detection (
	id INTEGER NOT NULL,
	img_id INTEGER,
	PRIMARY KEY (id),
	FOREIGN KEY(img_id) REFERENCES image (id)
);

CREATE TABLE annotation (
	id INTEGER NOT NULL,
	obj_type VARCHAR(100),
	left_x FLOAT,
	left_y FLOAT,
	length FLOAT,
	width FLOAT,
	detection_id INTEGER,
	PRIMARY KEY (id),
	FOREIGN KEY(detection_id) REFERENCES detection (id)
);


CREATE TABLE feedback (
	id INTEGER NOT NULL,
	corr_obj_type VARCHAR(100),
	corr_left_x FLOAT,
	corr_left_y FLOAT,
	corr_length FLOAT,
	corr_width FLOAT,
	detection_id INTEGER,
	PRIMARY KEY (id),
	FOREIGN KEY(detection_id) REFERENCES detection (id)
)
