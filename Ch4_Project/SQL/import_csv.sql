/***************************
 Script for updating OSM tables

****************************/

--empty existing tables
truncate ways_nodes cascade;
truncate nodes_tags cascade;
truncate nodes cascade;
truncate ways_tags cascade;
truncate ways cascade;

--insert nodes;
\COPY nodes(id,lat,lon,username,uid,version,changeset,ts) FROM 'nodes.csv' WITH (FORMAT 'csv', DELIMITER ',', HEADER);
\COPY ways(id,username,uid,version,changeset,ts) FROM 'ways.csv' WITH (FORMAT 'csv', DELIMITER ',', HEADER);
\COPY nodes_tags(id,key,value,type) FROM 'nodes_tags.csv' WITH (FORMAT 'csv', DELIMITER ',', HEADER);
\COPY ways_tags(id,key,value,type) FROM 'ways_tags.csv' WITH (FORMAT 'csv', DELIMITER ',', HEADER);
\COPY ways_nodes(id,node_id,position) FROM 'ways_nodes.csv' WITH (FORMAT 'csv', DELIMITER ',', HEADER);
