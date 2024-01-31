import mysql.connector
from dotenv import load_dotenv # for local use
import os
import Board

# Class SQLDatabase is used to connect to MySQL DB
# to create, read, update, and delete data from the DB
class Connect2DB:

    # Constructor: set up connection to MySQL DB
    #
    # @PARMS
    #  db: variable use to connect to MySQL DB
    #
    # return: None
    def __init__(self):
        
        # set up connection to MySQL DB
        self.conn = self.set_Connection()
        
        # set up cursor to execute SQL queries
        self.cursor = self.conn.cursor(buffered=True)

    # Destructor: close connection to MySQL DB
    def __del__(self):
        self.conn.close()

    # Set up the connection to MySQL DB. We will be using port 33306
    # on our machine to connect to the DB port 3306 on the VM 
    # (which is already configured when we SSH)
    #
    # @PARMS
    #   conn: variable use to connect to MySQL DB
    #
    # NOTE: password should be in CI/CD pipeline in GitLab (same var. name)
    def set_Connection(self):
        
        # This is for local .env file (not in GitLab)
        load_dotenv() 
        
        try:
            # Process "conn" to connect to MySQL DB with these options
            conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password=os.environ.get("MYSQL_PASSWORD"),
                database="chess",
                port="33306"
            )

            if conn.is_connected():
                # return conn for further processing
                return conn
            
        except Exception as e:
            print(f"Error connecting to MySQL database: {e}")
            return None
    
        
    # engine Table: get username from DB using engine_Code
    # 
    # @PARMS:
    #   idEngine: engine Primary Key use to retireved username
    def get_username(self, idEngine):
        # SQL query to get username from DB
        sql = "SELECT username FROM users WHERE idEngine = %s"
        # execute query
        self.cursor.execute(sql, (idEngine))
        # get result from query
        result = self.cursor.fetchone()
        # return result
        return result
    
    # Set history table in SQL DB with the following parameters
    #
    # @PARMS:
    #   FenString: FEN string of the board
    #   moveHistory: move history of the board
    #   idEngine: engine Primary Key
    #   idOpeningBook: opening book Primary Key
    #   idEndGame: end game Primary Key
    def set_History(self, moveHistory: str, FenString: str, name: str, code: str, idOpeningBook: int = -1):        
        sql = "SELECT idEngine FROM engine WHERE EngineCode = %s and Username = %s"
        self.cursor.execute(sql, (code, name))
        idEngine = self.cursor.fetchone()[0]
        
        # idOpeningBook is get from SQL DB
        # TODO: get idOpeningBook from SQL DB
        
        # SQL query to insert into history table
        sql = "INSERT INTO history (FenString, moveHistory, idEngine, idOpeningBook) VALUES (%s, %s, %s, %s)"
        # execute query
        self.cursor.execute(sql, (FenString, moveHistory, idEngine, idOpeningBook))
        # commit changes to DB
        self.conn.commit()
        # return result
        return self.cursor.lastrowid