import Connect2DB
import uuid

# Demo1 Function: Asks for a username or alias
# to be put into the database server.
#
# Input: a string name or alias

if __name__ == "__main__":

    # initialize connection
    connection = None

    # call function to set up connection
    connection = Connect2DB.set_Connection(connection)

    # set cursor for DB
    cursor = connection.cursor()

    # get unique identifier integer from uuid lib
    engine_code = str(uuid.uuid4().int)

    try:
        # run sql statement
        SQLStmt = "INSERT INTO engine(EngineCode) VALUES (%s)"

        # append to list
        val = []
        val.append(engine_code)
        # execute, commit, and close connection to sql db
        cursor.execute(SQLStmt, val)

        print(f"{cursor.rowcount} row(s) affected.")

    except Exception as e:
        print(f"Error: {e}")
    connection.commit()
    connection.close()






