SELECT U.username, G.score, G.message
FROM (
	SELECT grades.uid, grades.score, grades.message, grades.gid
	FROM grades
	WHERE grades.aid=:aid) AS G
JOIN (
	SELECT uid, username
	FROM users) AS U
ON G.uid=U.uid
ORDER BY G.gid ASC
