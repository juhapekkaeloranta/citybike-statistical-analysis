-- Table: citybikeschema.availability

-- DROP TABLE citybikeschema.availability;

CREATE TABLE citybikeschema.availability
(
  stationid integer,
  "time" timestamp without time zone,
  avlbikes integer,
  bar bigserial NOT NULL
)
WITH (
  OIDS=FALSE
);
ALTER TABLE citybikeschema.availability
  OWNER TO postgres;