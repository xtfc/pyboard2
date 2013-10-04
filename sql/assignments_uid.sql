SELECT assignments.*
FROM assignments, entries
WHERE (assignments.cid=entries.cid)
AND (entries.uid=:uid)
