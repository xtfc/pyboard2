SELECT courses.cid, courses.displayname, entries.level
FROM courses, entries
WHERE (courses.cid=entries.cid)
AND (entries.uid=:uid)
ORDER BY courses.cid ASC
