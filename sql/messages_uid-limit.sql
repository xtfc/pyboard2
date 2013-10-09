SELECT M.*, C.*
FROM (
	SELECT messages.*
	FROM messages, entries
	WHERE (messages.cid=entries.cid)
	AND (entries.uid=:uid)) AS M
JOIN (
	SELECT cid, name
	FROM courses) AS C
ON M.cid=C.cid
ORDER BY M.mid DESC
LIMIT :limit
