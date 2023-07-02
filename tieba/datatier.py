def select_one_row(dbConn, sql, parameters=None):
    if parameters is None:
        parameters = []

    dbCursor = dbConn.cursor()

    try:
        dbCursor.execute(sql, parameters)
        row = dbCursor.fetchone()
        if row is None:
            return ()
        return row
    except Exception as err:
        print('select_one_row failed:', err)
        return None
    finally:
        dbCursor.close()


def select_n_rows(dbConn, sql, parameters=None):
    if parameters is None:
        parameters = []

    dbCursor = dbConn.cursor()

    try:
        dbCursor.execute(sql, parameters)
        rows = dbCursor.fetchall()
        if rows is None:
            return ()
        return rows
    except Exception as err:
        print('select_n_rows failed:', err)
        return None
    finally:
        dbCursor.close()


def perform_action(dbConn, sql, parameters=None):
    if parameters is None:
        parameters = []

    dbCursor = dbConn.cursor()
    #dbCursor.execute("PRAGMA foreign_keys = ON")
    try:
        dbCursor.execute(sql, parameters)
        row = dbCursor.rowcount
        return row
    except Exception as err:
        print('perform_action failed:', err)
        return -1
    finally:
        dbCursor.close()


def contain(dbConn, sql, parameters=None):
    if parameters is None:
        parameters = []
    dbCursor = dbConn.cursor()
    try:
        dbCursor.execute(sql, parameters)
        rows = dbCursor.fetchall()
        if rows is None:
            return False
        return True
    except Exception as err:
        print('contain failed:', err)
        return False
    finally:
        dbCursor.close()
