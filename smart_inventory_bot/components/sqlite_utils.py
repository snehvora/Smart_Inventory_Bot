import sqlite3

def sqlite_exc(
        query : str
    ):

    print("Start Establishing Connection")
    try:
        con = sqlite3.connect('/Users/snehvora/Desktop/smart_inventory_bot/data/sqlite.db')
        print("Connection Established")
        curr = con.cursor()
        l_data = []
        print("Query Execution started")
        curr.execute(query)
        print("Query Executed")
        rows = curr.fetchall()
        for row in rows:
            l_data.append(row)
        con.close()
        return l_data
    except sqlite3.Error as e:
        return "error"

