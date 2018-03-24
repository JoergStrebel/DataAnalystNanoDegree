drop table ways_nodes cascade;
drop table ways_tags cascade;
drop table nodes_tags cascade;
drop table nodes cascade;
drop table ways cascade;


CREATE TABLE nodes (
    id bigint PRIMARY KEY NOT NULL,
    lat REAL,
    lon REAL,
    username TEXT,
    uid INTEGER,
    version INTEGER,
    changeset bigint,
    ts timestamp with time zone
);

CREATE TABLE nodes_tags (
    id bigint,
    key TEXT,
    value TEXT,
    type TEXT,
    FOREIGN KEY (id) REFERENCES nodes(id)
);

CREATE TABLE ways (
    id bigint PRIMARY KEY NOT NULL,
    username TEXT,
    uid INTEGER,
    version TEXT,
    changeset bigint,
    ts timestamp with time zone
);

CREATE TABLE ways_tags (
    id bigint NOT NULL,
    key TEXT NOT NULL,
    value TEXT NOT NULL,
    type TEXT,
    FOREIGN KEY (id) REFERENCES ways(id)
);

CREATE TABLE ways_nodes (
    id bigint NOT NULL,
    node_id bigint NOT NULL,
    position bigint NOT NULL,
    FOREIGN KEY (id) REFERENCES ways(id),
    FOREIGN KEY (node_id) REFERENCES nodes(id)
);
