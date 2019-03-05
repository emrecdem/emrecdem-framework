import sqlite3

def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)

    return None

def create_table(conn, create_table_sql):
    """ create a table from the create_table_sql statement
    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :return:
    """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)

def main(databasefile):
    # Note time in text datatype, which will facilitate ISO8601 "YYYY-MM-DD HH:MM:SS.SSS"
    sql_create_participants_table = """ CREATE TABLE IF NOT EXISTS participants (
                                        id integer PRIMARY KEY,
                                        age real
                                    ); """

    sql_create_experiments_table = """ CREATE TABLE IF NOT EXISTS experiments (
                                        id integer PRIMARY KEY,
                                        name text NOT NULL
                                    ); """
    sql_create_videofeatures_table = """ CREATE TABLE IF NOT EXISTS videofeatures (
                                        id integer PRIMARY KEY,
                                        participant_id integer NOT NULL,
                                        experiment_id text NOT NULL,
                                        time text,
                                        AU01r real, AU02r real, AU04r real,
                                        AU05r real, AU06r real, AU07r real,
                                        AU09r real, AU10r real, AU12r real,
                                        AU14r real, AU15r real, AU17r real,
                                        AU20r real, AU23r real, AU25r real,
                                        AU26r real, AU45r real, AU01c real,
                                        AU02c real, AU04c real, AU05c real,
                                        AU06c real, AU07c real, AU09c real,
                                        AU10c real, AU12c real, AU14c real,
                                        AU15c real, AU17c real, AU20c real,
                                        AU23c real, AU25c real, AU26c real,
                                        AU28c real, AU45c real,
                                        FOREIGN KEY (participant_id) REFERENCES participants (id),
                                        FOREIGN KEY (experiment_id) REFERENCES experiments (id)
                                    ); """

    sql_create_audiofeatures_table = """ CREATE TABLE IF NOT EXISTS audiofeatures (
                                        id integer PRIMARY KEY,
                                        participant_id integer NOT NULL,
                                        experiment_id text NOT NULL,
                                        time text,
                                        pitch real,
                                        rmse real,
                                        zcrate real,
                                        FOREIGN KEY (participant_id) REFERENCES participants (id),
                                        FOREIGN KEY (experiment_id) REFERENCES experiments (id)
                                    ); """

    sql_create_facslabels_table = """ CREATE TABLE IF NOT EXISTS facslabels (
                                        id integer PRIMARY KEY,
                                        name text NOT NULL
                                    ); """

    sql_create_facsencoding_table = """CREATE TABLE IF NOT EXISTS tasks (
                                    id integer PRIMARY KEY,
                                    participant_id integer NOT NULL,
                                    experiment_id integer NOT NULL,
                                    timestamp text,
                                    emotion_id integer NOT NULL,
                                    FOREIGN KEY (participant_id) REFERENCES participants (id),
                                    FOREIGN KEY (experiment_id) REFERENCES experiments (id),
                                    FOREIGN KEY (emotion_id) REFERENCES facslabels (id)
                                );"""

    # create a database connection
    conn = create_connection(databasefile)
    if conn is not None:
        # create participants table
        create_table(conn, sql_create_participants_table)
        # create experiments table
        create_table(conn, sql_create_experiments_table)
        create_table(conn, sql_create_videofeatures_table)
        create_table(conn, sql_create_audiofeatures_table)
        create_table(conn, sql_create_facslabels_table)
        create_table(conn, sql_create_facsencoding_table)
    else:
        print("Error! cannot create the database connection.")


def createdatabase(databasefile):
    if __name__ == '__main__':
        main(databasefile=databasefile)
    main(databasefile=databasefile)


def checkdbcontent(databasefile):
    conn = create_connection(databasefile) # create connection
    cur = conn.cursor() # create cursor
    results = cur.execute("select * from audiofeatures limit 3;").fetchall()
    rowcount = cur.execute("select count(*) from audiofeatures;").fetchall()
    colnames = cur.execute("PRAGMA table_info(audiofeatures);").fetchall()
    print("\nTop 3 rows of audiofeatures table:")
    print(results)
    print("\nRow count:")
    print(rowcount[0][0])
    print("\nColumn names:")
    print(colnames)
    results = cur.execute("select * from videofeatures limit 3;").fetchall()
    rowcount = cur.execute("select count(*) from videofeatures;").fetchall()
    colnames = cur.execute("PRAGMA table_info(videofeatures);").fetchall()
    print("\nTop 3 rows of videofeatures table:")
    print(results)
    print("\nRow count:")
    print(rowcount[0][0])
    print("\nColumn names:")
    print(colnames)
    cur.close()
    conn.close()

def features2db(audio_features, video_features, databasefile, deleteDataBaseEntries = False):
    conn = create_connection(databasefile) # create connection
    cur = conn.cursor() # create cursor

    # delete contents of table for testing purposes, later we obviously do not want to do this
    if (deleteDataBaseEntries == True):
        deleterows = cur.execute("DELETE FROM videofeatures;").fetchall()
        deleterows = cur.execute("DELETE FROM audiofeatures;").fetchall()
    # move time_series pandas data frame to the database
    audio_features.to_sql("audiofeatures", conn, index= False, if_exists="append") #"replace"

    # move time_series pandas data frame to the database
    video_features.to_sql("videofeatures", conn, index=False,if_exists="append") #"replace"
    cur.close()
    conn.close()
