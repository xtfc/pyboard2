SELECT A.*, C.*
FROM (
	SELECT *
	FROM assignments
	WHERE (assignments.cid=:cid)
) AS A
JOIN (
	SELECT *
	FROM courses
) AS C
ON A.cid=C.cid
ORDER BY A.name ASC
