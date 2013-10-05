SELECT courses.cid, courses.name, courses.displayname, entries.level, (courses.cid=:cid) as visible
FROM courses, entries
WHERE (courses.cid=entries.cid)
AND (entries.uid=:uid)
