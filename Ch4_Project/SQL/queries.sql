/* SQL requests for OSM data wrangling project */
 
--Number of nodes
SELECT COUNT(*) FROM nodes;

-- Number of ways
SELECT COUNT(*) FROM ways;

--Number of unique users
SELECT COUNT(DISTINCT(e.uid)) FROM (SELECT uid FROM nodes UNION ALL SELECT uid FROM ways) e;

--Top 10 contributing users
SELECT e.username, COUNT(*) as num FROM 
       (SELECT username FROM nodes UNION ALL SELECT username FROM ways) e 
GROUP BY e.username 
ORDER BY num DESC 
LIMIT 10;

-- Number of users appearing only once (having 1 post)
SELECT COUNT(*) FROM 
       (SELECT e.username, COUNT(*) as num FROM 
       	      (SELECT username FROM nodes UNION ALL SELECT username FROM ways) e 
       GROUP BY e.username HAVING COUNT(*)=1) u;

-- Size of the project database 
select pg_database_size('udacity')/(1024*1024) megabytes;

-- TODO, FIXME Tags
select key, count(key) from (select key from nodes_tags union all select key from ways_tags) v_tags
where key like 'FIXME' or key like 'fixme' or key like 'TODO'  group by key;


-- Well-formedness of email address
SELECT value from 
(select key,value  from nodes_tags union all select key, value from ways_tags) v_tags where 
key='email' and 
not value ~* '.+@.+';

-- Tag keys
SELECT key, count(*) num from 
(select key,value  from nodes_tags union all select key, value from ways_tags) v_tags 
group by key
order by num desc;

-- types of amenities
SELECT value, COUNT(*) as num
FROM nodes_tags
WHERE key='amenity'
GROUP BY value
ORDER BY num DESC
LIMIT 10;

-- types of hunting stands
select  key,value from (SELECT id 
FROM nodes_tags
WHERE key='amenity' and value='hunting_stand') v_hs 
inner join 
nodes_tags t2 on t2.id=v_hs.id 
where
not t2.key='amenity' and not t2.value='hunting_stand' and not key='fixme' and not key='ref' and not key='source' and not t2.key='hunting_stand'
group by key, value
order by key ;


