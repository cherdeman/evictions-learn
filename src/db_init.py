import os
import logging
from src.db_client import DBClient
import src.db_statements

logger = logging.getLogger('evictionslog')

class DBInit():
    """Clear and initialize the evictions database."""

    def __init__(self):
        self.db = DBClient()

    def evictions_init(self):
        """Clear and initialize the evictions table(s)."""

        logger.info("Dropping tables...")
        self.db.write([db_statements.DROP_TABLE_BLOCKGROUP])

        logger.info("Creating tables...")
        self.db.write([db_statements.CREATE_TABLE_BLOCKGROUP])

        logger.info("Creating indexes...")
        self.db.write([
            db_statements.IDX_YEAR,
            db_statements.IDX_STATE,
            db_statements.IDX_STATE_YEAR,
            db_statements.IDX_GEOID,
            db_statements.IDX_GEOID_YEAR,
            db_statements.IDX_EVICTIONS
        ])

        logger.info("Tables & indexes committed.")

        logger.info("Copying CSV data to evictions db...")
        self.db.copy('C:/Users/Justin Cohler/output.csv', db_statements.COPY_CSV_BLOCKGROUP)
        logger.info("Records committed.")

    def geo_init(self):
        """Clear and initialize the geospatial table(s)."""

        self.db.write([
            db_statements.CREATE_EXT_POSTGIS,
            db_statements.CREATE_EXT_FUZZY,
            db_statements.CREATE_EXT_TIGER,
            db_statements.CREATE_EXT_POSTGIS_TOP,
            db_statements.DROP_F_EXEC,
            db_statements.CREATE_F_EXEC,
            db_statements.ALTER_SPATIAL_REF_SYS.format(self.db.DB_USER),
            db_statements.INSERT_SPATIAL_REF_SYS
        ])

    def census_shp(geography):
        """Read shapes for a given geography."""

        shp_read = "shp2pgsql -s 4269:4326 -W 'latin1' data/tl_2010_us_{}10/tl_2010_us_{}10.shp evictions.census_{}_shp | psql {} -U {} -W {} -p {} -h {}".format(geography, geography, geography,'evictions', self.db.DB_USER, self.db.DB_PASSWORD, self.db.DB_PORT, self.db.DB_HOST)
        os.system(shp_read)

    def group_by_state():
        """Clear and initialize the evictions_state table."""

        self.db.write([
            db_statements.DROP_TABLE_EVICTIONS_STATE,
            db_statements.CREATE_TABLE_EVICTIONS_STATE,
            db_statements.INSERT_EVICTIONS_STATE
        ])

if __name__=="__main__":
    initializer = DBInit()
    initializer.evictions_init()
    initializer.geo_init()
