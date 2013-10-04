SELECT courses.cid, courses.name, courses.displayname, entries.level
FROM courses, entries
WHERE (courses.cid=entries.cid)
AND (entries.uid=:uid)
