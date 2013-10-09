SELECT M.*, C.*
FROM (
	SELECT messages.*
	FROM messages, entries
	WHERE (messages.cid=entries.cid)
	AND (entries.uid=:uid)
	AND (entries.cid=:cid)) AS M
JOIN (
	SELECT cid, displayname
	FROM courses) AS C
ON M.cid=C.cid
ORDER BY M.mid DESC
