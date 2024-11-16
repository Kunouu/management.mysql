import psycopg2

class PostgreSqlClient:

    def __init__(self, username: str, password: str, host: str, database: str):
        self.sqlClient = psycopg2.connect(
            host=host,
            user=username,
            password=password,
            dbname=database
        )
        self.cursor = self.sqlClient.cursor()

    def insertEmployee(self, name: str, phoneNumber: str, email: str, country: str, city: str, salary: str):
        insertQuery = """
        INSERT INTO employeedetails (name, phoneNumber, email, country, city, salary)
        VALUES (%s, %s, %s, %s, %s, %s)
        """
        self.cursor.execute(insertQuery, (name, phoneNumber, email, country, city, salary))
        self.sqlClient.commit()

    def findEmployee(self, method: str, value: str):
        queries = {
            'Id': "SELECT * FROM employeedetails WHERE id = %s",
            'Имя': "SELECT * FROM employeedetails WHERE name LIKE %s",
            'Мобильный телефон': "SELECT * FROM employeedetails WHERE phoneNumber = %s",
            'Email': "SELECT * FROM employeedetails WHERE email = %s",
            'Страна': "SELECT * FROM employeedetails WHERE country = %s",
            'Город': "SELECT * FROM employeedetails WHERE city = %s"
        }

        if method in queries:
            query = queries[method]
            param = int(value) if method == 'Id' else ('%' + value + '%' if method == 'Имя' else value)
            self.cursor.execute(query, (param,))
            return self.cursor.fetchall()
        else:
            raise ValueError("Недопустимый метод поиска")

    def deleteEmployee(self, method: str, value: str):
        queries = {
            'Id': "DELETE FROM employeedetails WHERE id = %s",
            'Имя': "DELETE FROM employeedetails WHERE name LIKE %s",
            'Мобильный телефон': "DELETE FROM employeedetails WHERE phoneNumber = %s",
            'Email': "DELETE FROM employeedetails WHERE email = %s"
        }

        if method in queries:
            query = queries[method]
            param = int(value) if method == 'Id' else ('%' + value + '%' if method == 'Имя' else value)
            self.cursor.execute(query, (param,))
            self.sqlClient.commit()
        else:
            raise ValueError("Недопустимый метод удаления")

    def updateEmployee(self, method: str, value: str, newValues: dict):
        try:
            if method == 'Id':
                condition = "id = %s"
                param = int(value)  # Для ID приводим значение к int
            elif method == 'Имя':
                condition = "name LIKE %s"
                param = '%' + value + '%'  # Для имени используем шаблон поиска
            else:
                raise ValueError("Недопустимый метод обновления")
            
            updateQuery = f"""
            UPDATE employeedetails
            SET 
                name = %s, 
                phoneNumber = %s, 
                email = %s, 
                country = %s, 
                city = %s, 
                salary = %s
            WHERE {condition}
            """
            
            # Выполняем запрос
            self.cursor.execute(updateQuery, (
                newValues.get('name'),
                newValues.get('phoneNumber'),
                newValues.get('email'),
                newValues.get('country'),
                newValues.get('city'),
                newValues.get('salary'),
                param
            ))

            # Фиксируем изменения в БД
            self.sqlClient.commit()
            print("Обновление прошло успешно.")
        except Exception as e:
            # В случае ошибки откатываем транзакцию
            self.sqlClient.rollback()
            print(f"Ошибка при обновлении сотрудника: {e}")


    def getAllEmployees(self):
        query = "SELECT * FROM employeedetails"
        self.cursor.execute(query)
        return self.cursor.fetchall()
