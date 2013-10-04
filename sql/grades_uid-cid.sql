SELECT T2.username, T1.name, T1.body, T1.score, T1.points, T1.cid
FROM (
	SELECT grades.uid, assignments.name, assignments.body, grades.score, assignments.points, assignments.cid
	FROM users, assignments, grades, entries
	WHERE ((grades.uid=users.uid) OR (entries.level > 0))
	AND (grades.aid=assignments.aid)
	AND (assignments.cid=entries.cid)
	AND (entries.uid=users.uid)
	AND (users.uid=:uid)
	AND (entries.cid=:cid)
	ORDER BY assignments.cid) AS T1
JOIN (
	SELECT users.uid, users.username
	FROM users) AS T2
ON T1.uid=T2.uid
