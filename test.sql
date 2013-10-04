INSERT INTO users(username, name, email) VALUES('john', 'John', 'john@pyboard.com');
INSERT INTO users(username, name, email) VALUES('jess', 'Jessica', 'jess@pyboard.com');
INSERT INTO users(username, name, email) VALUES('tyler', 'Tyler', 'tyler@pyboard.com');
INSERT INTO users(username, name, email) VALUES('phil', 'Philip', 'phil@pyboard.com');

INSERT INTO courses(name) VALUES('CS 140');
INSERT INTO courses(name) VALUES('CS 320');

INSERT INTO entries(uid, cid, level) VALUES(1, 1, 1); -- John is a CA for CS 140
INSERT INTO entries(uid, cid, level) VALUES(1, 2, 0); -- John is a student for CS 320
INSERT INTO entries(uid, cid, level) VALUES(2, 1, 0); -- Jess is a student for CS 140
INSERT INTO entries(uid, cid, level) VALUES(3, 2, 2); -- Tyler is a TA for CS 320
INSERT INTO entries(uid, cid, level) VALUES(4, 1, 2); -- Phil is a TA for CS 140

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

INSERT INTO grades(uid, aid, score) VALUES(1, 3, 9); -- John got a 9 on Lab 1 :: CS 320
INSERT INTO grades(uid, aid, score) VALUES(1, 4, 10); -- John got a 10 on Lab 2 :: CS 320
INSERT INTO grades(uid, aid, score) VALUES(1, 5, 24); -- John got a 24 on Exam 1 :: CS 320
INSERT INTO grades(uid, aid, score) VALUES(1, 1, 7); -- John got a 7 on Lab 1 :: CS 140
INSERT INTO grades(uid, aid, score) VALUES(2, 1, 10); -- Jess got a 10 on Lab 1 :: CS 140
INSERT INTO grades(uid, aid, score) VALUES(2, 2, 19); -- Jess got a 19 on Exam 1 :: CS 140
