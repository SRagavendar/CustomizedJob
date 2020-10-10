def data_table_creation(cursor, connection_to_db):
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS data(
    question TEXT NOT NULL,
    answer TEXT NULL,
    question_type TEXT NOT NULL,
    question_type_answers TEXT NULL,
    PRIMARY KEY(question)
    );
    """)
    connection_to_db.commit()

def get_file_contents(db_cursor):

    db_cursor.execute("""SELECT * FROM data""")
    db_rows = db_cursor.fetchall()
    return {row[0]: row[1] for row in db_rows if row != []}