import pymysql

class DBConnectivity:
    
    @staticmethod
    def getConnection(hostname,username,password,database):
        con = pymysql.connect(host=hostname,user=username,password=password,db=database)
        return con
    
    @staticmethod
    def getQueryResult(connection,query):
        cursor = connection.cursor()
        cursor.execute(query)
        return cursor
    
    @staticmethod
    def updateDatabase(connection,query):
        cursor = connection.cursor()
        cursor.execute(query)
        connection.commit()
        cursor.close()
    
    @staticmethod
    def closeConnection(connection):
        if connection != None:
            connection.close()
        
    