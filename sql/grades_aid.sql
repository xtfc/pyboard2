SELECT G.gid, U.username, G.score, G.message, G.timestamp
FROM (
	SELECT *
	FROM grades
	WHERE (grades.aid=:aid)
) AS G
JOIN (
	SELECT *
	FROM users
) AS U
ON G.uid=U.uid
ORDER BY G.gid ASC
