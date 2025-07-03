import psycopg2
from psycopg2.extras import RealDictCursor

# --- Default Postgres credentials ---
DB_CONFIG = {
    "dbname": "postgres",
    "user": "postgres",
    "password": "postgres",
    "host": "localhost",
    "port": 5432,
}
SAMPLE_ROW_LIMIT = 5


def connect():
    return psycopg2.connect(**DB_CONFIG)


def list_tables(conn):
    with conn.cursor() as cur:
        cur.execute(
            """
            SELECT table_name
            FROM information_schema.tables
            WHERE table_schema = 'public'
              AND table_type = 'BASE TABLE';
        """
        )
        return [row[0] for row in cur.fetchall()]


def get_table_columns(conn, table_name):
    with conn.cursor() as cur:
        cur.execute(
            """
            SELECT column_name, data_type, is_nullable
            FROM information_schema.columns
            WHERE table_schema = 'public'
              AND table_name = %s
            ORDER BY ordinal_position;
        """,
            (table_name,),
        )
        return cur.fetchall()


def get_foreign_keys(conn):
    with conn.cursor() as cur:
        cur.execute(
            """
            SELECT
                conrelid::regclass AS table_from,
                a.attname AS column_from,
                confrelid::regclass AS table_to,
                af.attname AS column_to
            FROM
                pg_constraint c
            JOIN pg_attribute a
              ON a.attnum = ANY(c.conkey) AND a.attrelid = c.conrelid
            JOIN pg_attribute af
              ON af.attnum = ANY(c.confkey) AND af.attrelid = c.confrelid
            WHERE c.contype = 'f';
        """
        )
        return cur.fetchall()


def get_sample_rows(conn, table_name, limit=SAMPLE_ROW_LIMIT):
    with conn.cursor(cursor_factory=RealDictCursor) as cur:
        try:
            cur.execute(f'SELECT * FROM public."{table_name}" LIMIT %s;', (limit,))
            return cur.fetchall()
        except Exception as e:
            return [f"Error fetching rows: {e}"]


def main():
    conn = connect()

    tables = list_tables(conn)

    for table in tables:

        for column_name, data_type, is_nullable in get_table_columns(conn, table):
            nullability = "NULL" if is_nullable == "YES" else "NOT NULL"

        rows = get_sample_rows(conn, table)
        for row in rows:
            pass


    for from_table, from_col, to_table, to_col in get_foreign_keys(conn):
        pass")

    conn.close()


if __name__ == "__main__":
    main()
