import mysql.connector

class mySqlClient:

    def __init__(self, username: str, password: str, host: str, database: str):
        sqlClient = mysql.connector.connect(  
            host=host,
            user=username,
            password=password,
            database=database
        )
        self.sqlClient = sqlClient
        self.cursor = sqlClient.cursor()

    def insertEmployee(self, name: str, phoneNumber: str, email: str, country: str, city: str, salary: str):
        insertQuery = "INSERT INTO employeedetails (name, phoneNumber, email, country, city, salary) VALUES (%s, %s, %s, %s, %s, %s)"
        self.cursor.execute(insertQuery, (name, phoneNumber, email, country, city, salary))
        self.sqlClient.commit()

    def findEmployee(self, method: str, value: str):
        idQuery = "SELECT * FROM employeedetails WHERE id = %s"
        nameQuery = "SELECT * FROM employeedetails WHERE name LIKE %s"
        phoneQuery = "SELECT * FROM employeedetails WHERE mobile_phone = %s"
        emailQuery = "SELECT * FROM employeedetails WHERE email = %s"
        countryQuery = "SELECT * FROM employeedetails WHERE country = %s"
        cityQuery = "SELECT * FROM employeedetails WHERE city = %s"
        
        if method == 'Id':
            self.cursor.execute(idQuery, (int(value),))
        elif method == 'Имя':
            self.cursor.execute(nameQuery, ('%' + value + '%',))
        elif method == 'Мобильный телефон':
            self.cursor.execute(phoneQuery, (value,))
        elif method == 'Email':
            self.cursor.execute(emailQuery, (value,))
        elif method == 'Страна':
            self.cursor.execute(countryQuery, (value,))
        elif method == 'Город':
            self.cursor.execute(cityQuery, (value,))
        
        return self.cursor.fetchall()

    def deleteEmployee(self, method: str, value: str):
        idQuery = "DELETE FROM employeedetails WHERE id = %s"
        nameQuery = "DELETE FROM employeedetails WHERE name LIKE %s"
        phoneQuery = "DELETE FROM employeedetails WHERE mobile_phone = %s"
        emailQuery = "DELETE FROM employeedetails WHERE email = %s"
        
        if method == 'Id':
            self.cursor.execute(idQuery, (int(value),))
        elif method == 'Имя':
            self.cursor.execute(nameQuery, ('%' + value + '%',))
        elif method == 'Мобильный телефон':
            self.cursor.execute(phoneQuery, (value,))
        elif method == 'Email':
            self.cursor.execute(emailQuery, (value,))
        
        self.sqlClient.commit()


    def updateEmployee(self, method: str, value: str, newValues: dict):
        updateQuery = """
            UPDATE employeedetails 
            SET name = %s, phoneNumber = %s, email = %s, country = %s, city = %s 
            WHERE {condition}
        """
        
        if method == 'Id':
            condition = "id = %s"
            query = updateQuery.format(condition=condition)
            self.cursor.execute(query, (newValues['name'], newValues['phoneNumber'], newValues['email'], newValues['country'], newValues['city'], int(value)))
        elif method == 'Имя':
            condition = "name LIKE %s"
            query = updateQuery.format(condition=condition)
            self.cursor.execute(query, (newValues['name'], newValues['phoneNumber'], newValues['email'], newValues['country'], newValues['city'], '%' + value + '%'))
        
        self.sqlClient.commit()
        
    def getAllEmployees(self):
        query = "SELECT * FROM employeedetails"
        self.cursor.execute(query)
        return self.cursor.fetchall()
