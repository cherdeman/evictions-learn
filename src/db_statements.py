"""DB Statements for the evictions-learn project."""

SET_SCHEMA = "set schema 'evictions';"

DROP_TABLE_BLOCKGROUP = "DROP TABLE IF EXISTS evictions.blockgroup;"

CREATE_TABLE_BLOCKGROUP = """CREATE TABLE evictions.blockgroup
(
  _id SERIAL PRIMARY KEY,
  state CHAR(2),
  geo_id CHAR(12),
  year SMALLINT,
  name VARCHAR(10),
  parent_location VARCHAR(100),
  population FLOAT,
  poverty_rate FLOAT,
  pct_renter_occupied FLOAT,
  median_gross_rent FLOAT,
  median_household_income FLOAT,
  median_property_value	FLOAT,
  rent_burden	FLOAT,
  pct_white	FLOAT,
  pct_af_am FLOAT,
  pct_hispanic FLOAT,
  pct_am_ind FLOAT,
  pct_asian FLOAT,
  pct_nh_pi FLOAT,
  pct_multiple FLOAT,
  pct_other FLOAT,
  renter_occupied_households FLOAT,
  eviction_filings FLOAT,
  evictions FLOAT,
  eviction_rate FLOAT,
  eviction_filing_rate FLOAT,
  imputed	BOOLEAN,
  subbed BOOLEAN
);"""

IDX_STATE_YEAR = "CREATE INDEX idx_state_year ON evictions.blockgroup (state, year);"
IDX_YEAR = "CREATE INDEX idx_year ON evictions.blockgroup (year);"
IDX_STATE = "CREATE INDEX idx_state ON evictions.blockgroup (state);"
IDX_EVICTIONS = "CREATE INDEX idx_evictions ON evictions.blockgroup (evictions);"
IDX_GEOID = "CREATE INDEX idx_geoid on evictions.blockgroup (geo_id)"


COPY_CSV_BLOCKGROUP = """COPY evictions.blockgroup(
state, geo_id, year, name, parent_location,population, poverty_rate, pct_renter_occupied,
median_gross_rent, median_household_income, median_property_value, rent_burden,
pct_white, pct_af_am, pct_hispanic, pct_am_ind, pct_asian, pct_nh_pi, pct_multiple,
pct_other, renter_occupied_households, eviction_filings, evictions, eviction_rate,
eviction_filing_rate, imputed, subbed)
FROM stdin WITH CSV HEADER DELIMITER as ','
"""

DROP_TABLE_EVICTIONS_STATE = "DROP TABLE IF EXISTS evictions_state;"

CREATE_TABLE_EVICTIONS_STATE = """CREATE TABLE evictions_state (state CHAR(2),
   stusps10 char(2),
   year SMALLINT,
   sum_evict FLOAT,
   avg_evict_rate float8,
   geom geometry);"""

INSERT_EVICTIONS_STATE = """INSERT INTO evictions.evictions_state (state, stusps10, year, sum_evict, avg_evict_rate, geom)
                SELECT state, stusps10, year, sum_evict, avg_evict_rate, geom from (
                    SELECT state, year, sum(evictions) as sum_evict, avg(eviction_rate) as avg_evict_rate
                    FROM evictions.blockgroup
                    GROUP BY state, year
                    ) as t1
                JOIN (SELECT stusps10, geom FROM evictions.census_state_shp) as t2 ON t1.state = t2.stusps10;"""

CREATE_EXT_POSTGIS = "CREATE EXTENSION postgis;"
CREATE_EXT_FUZZY = "create extension fuzzystrmatch;"
CREATE_EXT_TIGER = "create extension postgis_tiger_geocoder;"
CREATE_EXT_POSTGIS_TOP = "create extension postgis_topology;"

DROP_F_EXEC = "drop function if exists exec(text);"
CREATE_F_EXEC = "CREATE FUNCTION exec(text) returns text language plpgsql volatile AS $f$ BEGIN EXECUTE $1; RETURN $1; END; $f$;"
ALTER_SPATIAL_REF_SYS = "ALTER TABLE spatial_ref_sys OWNER TO {};"
INSERT_SPATIAL_REF_SYS = """INSERT into spatial_ref_sys (srid, auth_name, auth_srid, proj4text, srtext)
                            VALUES ( 102003, 'esri', 102003, '+proj=aea +lat_1=29.5 +lat_2=45.5 +lat_0=37.5 +lon_0=-96 +x_0=0 +y_0=0 +ellps=GRS80 +datum=NAD83 +units=m +no_defs ', 'PROJCS["USA_Contiguous_Albers_Equal_Area_Conic",GEOGCS["GCS_North_American_1983",DATUM["North_American_Datum_1983",SPHEROID["GRS_1980",6378137,298.257222101]],PRIMEM["Greenwich",0],UNIT["Degree",0.017453292519943295]],PROJECTION["Albers_Conic_Equal_Area"],PARAMETER["False_Easting",0],PARAMETER["False_Northing",0],PARAMETER["longitude_of_center",-96],PARAMETER["Standard_Parallel_1",29.5],PARAMETER["Standard_Parallel_2",45.5],PARAMETER["latitude_of_center",37.5],UNIT["Meter",1],AUTHORITY["EPSG","102003"]]');"""
