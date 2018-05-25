import json
import csv
import psycopg2
import os
import atexit
import logging
import db_statements

logger = logging.getLogger('evictionslog')


class DBClient():

    def __init__(self):

        if 'DB_USER' not in os.environ:
            resources_dir = os.path.dirname(__file__)
            secrets_file = os.path.join(resources_dir, '../resources/secrets.json')
            with open(secrets_file) as f:
                env = json.load(f)
            self.DB_USER = env['DB_USER']
            self.DB_PASSWORD = env['DB_PASSWORD']
            self.DB_HOST = env['DB_HOST']
            self.DB_PORT = env['DB_PORT']
        else:
            self.DB_USER = os.environ['DB_USER']
            self.DB_PASSWORD = os.environ['DB_PASSWORD']
            self.DB_HOST = os.environ['DB_HOST']
            self.DB_PORT = os.environ['DB_PORT']

        conn = psycopg2.connect(database="evictions", user=self.DB_USER,
                                password=self.DB_PASSWORD, host=self.DB_HOST, port=self.DB_PORT)
        logger.info("Connected to evictions DB.")
        self.conn = conn

        with self.conn.cursor() as cur:
            cur.execute(db_statements.SET_SCHEMA)
            cur.callproc("bg_get_chunk", ["bg_cursor"])
        self.cur = self.conn.cursor("bg_cursor")

        logger.info("Set schema to 'evictions'.")
        logger.info("Set background cursor.")
        atexit.register(self.exit)

    def write(self, statements, values=None):
        """Execute statements, close the cursor on exit (write-only)."""
        with self.conn.cursor() as cur:
            for statement in statements:
                cur.execute(statement)

        self.conn.commit()

    def read(self, statement, args=None):
        """Execute statement, fetchall returned rows."""
        l = []
        with self.conn.cursor() as cur:
            if not args:
                cur.execute(statement)
            else:
                cur.execute(statement, args)
            l = cur.fetchall()
        return l

    def copy(self, csv_path, statement, args=None):
        """Execute copy statement."""
        with open(csv_path, 'r') as f:
            cur = self.conn.cursor()
            cur.copy_expert(sql=statement, file=f)

        self.conn.commit()

    def exit(self):
        # self.conn.cursor.close()
        self.conn.close()
        logger.info("Connection closed.")
