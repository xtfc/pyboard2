SELECT M.*, C.*
FROM (
	SELECT *
	FROM messages
	WHERE (messages.cid=:cid)
) AS M
JOIN (
	SELECT *
	FROM courses
) AS C
ON M.cid=C.cid
ORDER BY M.mid DESC
