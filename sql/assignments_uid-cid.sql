SELECT A.*, C.name, C.displayname
FROM (
	SELECT assignments.*
	FROM assignments, entries
	WHERE (assignments.cid=entries.cid)
	AND (entries.uid=:uid)
	AND (entries.cid=:cid)) AS A
JOIN (
	SELECT cid, name, displayname
	FROM courses) AS C
ON A.cid=C.cid
ORDER BY A.name ASC
