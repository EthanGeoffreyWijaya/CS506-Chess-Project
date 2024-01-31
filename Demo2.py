import Connect2DB

# Demo Function: return games history
if __name__ == "__main__":

    # initialize connection
    connection = None

    # call function to set up connection
    connection = Connect2DB.set_Connection(connection)

    # set cursor for DB
    cursor = connection.cursor()

    # execute sql statement:
    cursor.execute("Select * FROM history")
    rows = cursor.fetchall()

    # print all user in DB
    for i in rows:
        print(i)
