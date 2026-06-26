import sqlite3
import pandas as pd


class DatabaseSample:
    def __init__(self, db_file='database.db'):
        self.db_file = db_file
        self.init_database()

    def get_connection(self):
        conn = sqlite3.connect(self.db_file)
        conn.row_factory = sqlite3.Row
        conn.execute('PRAGMA foreign_keys = ON')
        return conn

    def init_database(self):
        conn = self.get_connection()
        cursor = conn.cursor()

        cursor.execute("PRAGMA foreign_keys = ON")

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS proby (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                lab_nomer TEXT NOT NULL
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS granulometry (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                proba_id INTEGER NOT NULL,
                gran_10 DECIMAL(4,1),
                gran_5_10 DECIMAL(4,1),
                gran_5_2 DECIMAL(4,1),
                gran_2_1 DECIMAL(4,1),
                gran_1_0_5 DECIMAL(4,1),
                gran_0_5_0_25 DECIMAL(4,1),
                gran_0_25_0_10 DECIMAL(4,1),
                gran_0_10_0_05 DECIMAL(4,1),
                gran_0_05_0_01 DECIMAL(4,1),
                gran_0_01_0_002 DECIMAL(4,1),
                gran_0_002 DECIMAL(4,1),

                FOREIGN KEY (proba_id) REFERENCES proby(id)
                    ON DELETE CASCADE
                    ON UPDATE CASCADE
            )
        """)

        conn.commit()
        conn.close()

    def add_proby_and_granulometry_from_df(self, df: pd.DataFrame, sample_col: str = "lab_nomer"):
        required_cols = [
            sample_col,
            "gran_10",
            "gran_5_10",
            "gran_5_2",
            "gran_2_1",
            "gran_1_0_5",
            "gran_0_5_0_25",
            "gran_0_25_0_10",
            "gran_0_10_0_05",
            "gran_0_05_0_01",
            "gran_0_01_0_002",
            "gran_0_002"
        ]

        missing = [col for col in required_cols if col not in df.columns]
        if missing:
            raise ValueError(f"В DataFrame отсутствуют колонки: {missing}")

        conn = self.get_connection()
        cursor = conn.cursor()

        try:
            cursor.execute("PRAGMA foreign_keys = ON")

            insert_proba_sql = """
                INSERT INTO proby (lab_nomer)
                VALUES (?)
            """

            insert_gran_sql = """
                INSERT INTO granulometry (
                    proba_id,
                    gran_10,
                    gran_5_10,
                    gran_5_2,
                    gran_2_1,
                    gran_1_0_5,
                    gran_0_5_0_25,
                    gran_0_25_0_10,
                    gran_0_10_0_05,
                    gran_0_05_0_01,
                    gran_0_01_0_002,
                    gran_0_002
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """

            for row in df.itertuples(index=False):
                lab_nomer = getattr(row, sample_col)

                if pd.isna(lab_nomer):
                    continue

                lab_nomer = str(lab_nomer).strip()
                if not lab_nomer:
                    continue

                cursor.execute(insert_proba_sql, (lab_nomer,))
                proba_id = cursor.lastrowid

                cursor.execute(
                    insert_gran_sql,
                    (
                        proba_id,
                        None if pd.isna(getattr(row, "gran_10")) else getattr(row, "gran_10"),
                        None if pd.isna(getattr(row, "gran_5_10")) else getattr(row, "gran_5_10"),
                        None if pd.isna(getattr(row, "gran_5_2")) else getattr(row, "gran_5_2"),
                        None if pd.isna(getattr(row, "gran_2_1")) else getattr(row, "gran_2_1"),
                        None if pd.isna(getattr(row, "gran_1_0_5")) else getattr(row, "gran_1_0_5"),
                        None if pd.isna(getattr(row, "gran_0_5_0_25")) else getattr(row, "gran_0_5_0_25"),
                        None if pd.isna(getattr(row, "gran_0_25_0_10")) else getattr(row, "gran_0_25_0_10"),
                        None if pd.isna(getattr(row, "gran_0_10_0_05")) else getattr(row, "gran_0_10_0_05"),
                        None if pd.isna(getattr(row, "gran_0_05_0_01")) else getattr(row, "gran_0_05_0_01"),
                        None if pd.isna(getattr(row, "gran_0_01_0_002")) else getattr(row, "gran_0_01_0_002"),
                        None if pd.isna(getattr(row, "gran_0_002")) else getattr(row, "gran_0_002"),
                    )
                )

            conn.commit()

        except sqlite3.Error:
            conn.rollback()
            raise

        finally:
            conn.close()


# db = DatabaseSample("database.db")
#
# data = {
#     "lab_nomer": [155, 11],
#     "gran_10": [33, 11],
#     "gran_5_10": [155, 11],
#     "gran_5_2": [155, 11],
#     "gran_2_1": [155, 11],
#     "gran_1_0_5": [155, 11],
#     "gran_0_5_0_25": [155, 11],
#     "gran_0_25_0_10": [155, 11],
#     "gran_0_10_0_05": [155, 11],
#     "gran_0_05_0_01": [155, 11],
#     "gran_0_01_0_002": [155, 11],
#     "gran_0_002": [33, 11]
# }
#
# df_itog = pd.DataFrame(data)
#
# db.add_proby_and_granulometry_from_df(df_itog)






