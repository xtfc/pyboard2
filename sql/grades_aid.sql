SELECT U.username, G.score, G.message
FROM (
	SELECT grades.uid, grades.score, grades.message
	FROM grades
	WHERE grades.aid=:aid
	ORDER BY gid ASC) AS G
JOIN (
	SELECT uid, username
	FROM users) AS U
ON G.uid=U.uid
