INSERT INTO users(username, name, email) VALUES('john', 'John', 'john@pyboard.com');
INSERT INTO users(username, name, email) VALUES('jess', 'Jessica', 'jess@pyboard.com');
INSERT INTO users(username, name, email) VALUES('tyler', 'Tyler', 'tyler@pyboard.com');
INSERT INTO users(username, name, email) VALUES('phil', 'Philip', 'phil@pyboard.com');

INSERT INTO courses(name) VALUES('CS 140');
INSERT INTO courses(name) VALUES('CS 320');
INSERT INTO courses(name) VALUES('Masters');
INSERT INTO courses(name) VALUES('PhD');

INSERT INTO entries(uid, cid, level) VALUES(1, 1, 1); -- John is a CA for CS 140
INSERT INTO entries(uid, cid, level) VALUES(1, 2, 0); -- John is a student for CS 320
INSERT INTO entries(uid, cid, level) VALUES(2, 1, 0); -- Jess is a student for CS 140
INSERT INTO entries(uid, cid, level) VALUES(3, 2, 2); -- Tyler is a TA for CS 320
INSERT INTO entries(uid, cid, level) VALUES(3, 4, 0); -- Tyler is a student for PhD
INSERT INTO entries(uid, cid, level) VALUES(4, 1, 2); -- Phil is a TA for CS 140
INSERT INTO entries(uid, cid, level) VALUES(4, 3, 0); -- Phil is a student for Masters

INSERT INTO assignments(cid, points, name, body)
	VALUES(1, 10, 'Lab 1', 'CS 140');
INSERT INTO assignments(cid, points, name, body)
	VALUES(1, 20, 'Exam 1', 'CS 140');
INSERT INTO assignments(cid, points, name, body)
	VALUES(2, 10, 'Lab 1', 'CS 320');
INSERT INTO assignments(cid, points, name, body)
	VALUES(2, 10, 'Lab 2', 'CS 320');
INSERT INTO assignments(cid, points, name, body)
	VALUES(2, 30, 'Exam 1', 'CS 320');
INSERT INTO assignments(cid, points, name, body)
	VALUES(3, 100, 'Research', 'Masters');
INSERT INTO assignments(cid, points, name, body)
	VALUES(4, 100, 'Research', 'PhD');
INSERT INTO assignments(cid, points, name, body, due)
	VALUES(1, 10, 'Lab 2', 'CS 140', strftime('%s', 'now', '+1 month'));

INSERT INTO grades(uid, aid, score, timestamp)
	VALUES(1, 3, 9, strftime('%s', 'now')); -- John got a 9 on Lab 1 :: CS 320
INSERT INTO grades(uid, aid, score, timestamp)
	VALUES(1, 4, 10, strftime('%s', 'now')); -- John got a 10 on Lab 2 :: CS 320
INSERT INTO grades(uid, aid, score, timestamp)
	VALUES(1, 5, 24, strftime('%s', 'now')); -- John got a 24 on Exam 1 :: CS 320
INSERT INTO grades(uid, aid, score, timestamp)
	VALUES(1, 1, 7, strftime('%s', 'now')); -- John got a 7 on Lab 1 :: CS 140
INSERT INTO grades(uid, aid, score, timestamp)
	VALUES(2, 1, 10, strftime('%s', 'now')); -- Jess got a 10 on Lab 1 :: CS 140
INSERT INTO grades(uid, aid, score, timestamp)
	VALUES(2, 2, 19, strftime('%s', 'now')); -- Jess got a 19 on Exam 1 :: CS 140
INSERT INTO grades(uid, aid, score, timestamp)
	VALUES(3, 7, 27, strftime('%s', 'now')); -- Tyler got a 27 on Research :: PhD
INSERT INTO grades(uid, aid, score, timestamp)
	VALUES(4, 6, 37, strftime('%s', 'now')); -- Phil got a 37 on Research :: Masters

INSERT INTO messages(cid, title, body, timestamp)
	VALUES(1, 'CS 140 Message', 'These are like announcements. Should support *Markdown*.', strftime('%s', 'now'));
INSERT INTO messages(cid, title, body, timestamp)
	VALUES(2, 'CS 320 Message', 'Getting **fancy** in `here`.', strftime('%s', 'now'));
INSERT INTO messages(cid, title, body, timestamp)
	VALUES(3, 'Masters Message', 'And ***less*** fancy.', strftime('%s', 'now'));
INSERT INTO messages(cid, title, body, timestamp)
	VALUES(4, 'PhD Message', 'And even less fancy.', strftime('%s', 'now'));
