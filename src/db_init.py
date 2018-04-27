import json
import csv
import psycopg2
import os

# Create the main database table
here = os.path.dirname(__file__)
secrets_path = os.path.join(here, 'secrets.json')
env = json.load(open(secrets_path))

conn = psycopg2.connect(database="evictions", user=env['db_user'], password=env['db_password'], host=env['db_host'], port=env['db_port'], options=f'-c search_path=evictions')
cur = conn.cursor()

# Drop the TABLE
cur.execute("DROP TABLE evictions.blockgroup;")

# Create the TABLE
create_table_block_group = """CREATE TABLE evictions.blockgroup
(
  _id SERIAL PRIMARY KEY,
  state CHAR(2),
  geo_id CHAR(12),
  year SMALLINT,
  name VARCHAR(10),
  parent_location VARCHAR(100),
  population DECIMAL,
  poverty_rate DECIMAL,
  pct_renter_occupied DECIMAL,
  median_gross_rent DECIMAL,
  median_household_income DECIMAL,
  median_property_value	DECIMAL,
  rent_burden	DECIMAL,
  pct_white	DECIMAL,
  pct_af_am DECIMAL,
  pct_hispanic DECIMAL,
  pct_am_ind DECIMAL,
  pct_asian DECIMAL,
  pct_nh_pi DECIMAL,
  pct_multiple DECIMAL,
  pct_other DECIMAL,
  renter_occupied_households DECIMAL,
  eviction_filings DECIMAL,
  evictions DECIMAL,
  eviction_rate DECIMAL,
  eviction_filing_rate DECIMAL,
  imputed	BOOLEAN,
  subbed BOOLEAN
);"""

cur.execute(create_table_block_group)

conn.commit()

# INSERT all rows from dump
insert_stmnt = """INSERT INTO  evictions.blockgroup(
state, geo_id, year, name, parent_location,population, poverty_rate, pct_renter_occupied,
median_gross_rent, median_household_income, median_property_value, rent_burden,
pct_white, pct_af_am, pct_hispanic, pct_am_ind, pct_asian, pct_nh_pi, pct_multiple,
pct_other, renter_occupied_households, eviction_filings, evictions, eviction_rate,
eviction_filing_rate, imputed, subbed)
VALUES (
    %s, %s, %s, %s, %s,
    %s, %s, %s, %s, %s,
    %s, %s, %s, %s, %s,
    %s, %s, %s, %s, %s,
    %s, %s, %s, %s, %s,
    %s, %s
    );
"""

with open('C:/Users/Justin Cohler/output.csv', 'r') as f:
    reader = csv.reader(f)
    next(reader)  # Skip the header row.
    count = 50
    for row in reader:
        if count > 0:
            count = count -1
        else:
            break
        row = [x if x != '' else None for x in row]
        row[-2] = False if '0' else True
        row[-1] = False if '0' else True

        cur.execute(
            insert_stmnt,
            tuple(row)
        )
conn.commit()
