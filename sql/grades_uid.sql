SELECT U.username, C.name, C.displayname, GA.name, GA.body, GA.score, GA.points
FROM (
	SELECT grades.uid, grades.gid, assignments.name, assignments.body, grades.score, assignments.points, assignments.cid
	FROM users, assignments, grades, entries
	WHERE ((grades.uid=users.uid) OR (entries.level > 0))
	AND (grades.aid=assignments.aid)
	AND (assignments.cid=entries.cid)
	AND (entries.uid=users.uid)
	AND (users.uid=:uid)) AS GA
JOIN (
	SELECT uid, username
	FROM users) AS U
ON GA.uid=U.uid
JOIN (
	SELECT cid, name, displayname
	FROM courses) AS C
ON GA.cid=C.cid
ORDER BY GA.cid ASC, GA.gid ASC
