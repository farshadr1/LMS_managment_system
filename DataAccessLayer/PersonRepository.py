import pyodbc
from DataAccessLayer.db_access_settings import connection_string_sql_server

class PersonRepository:
    def __init__(self):
        self.conn_str = connection_string_sql_server

    def select_all(self):
        query = '''
            SELECT [FirstName], [LastName], [Gender], [NationalCode], [Birthdate],
                   [Mobile], [Education], [Address], Person.ID, [Photo]
            FROM Person
            JOIN Education on Person.EducationID = Education.ID;
        '''
        with pyodbc.connect(self.conn_str) as conn:
            cursor = conn.cursor()
            cursor.execute(query)
            return cursor.fetchall()

    def search(self, values):
        query = '''
            SELECT [FirstName], [LastName], [Gender], [NationalCode], [Birthdate],
                   [Mobile], [Education], [Address], Person.ID, [Photo]
            FROM Person
            JOIN Education on Person.EducationID = Education.ID
            WHERE [FirstName]=? or [LastName]=? or [Gender]=? or [NationalCode]=? or [Birthdate]=? or
                  [Mobile]=? or [Education]=? or [Address]=? or Person.ID=?;
        '''
        with pyodbc.connect(self.conn_str) as conn:
            cursor = conn.cursor()
            cursor.execute(query, values)
            return cursor.fetchall()

    def insert(self, values):
        query = '''
            INSERT INTO Person([FirstName], [LastName], [Birthdate], [NationalCode], [Gender],
                               [Address], [Mobile], [EducationID], [Photo])
            OUTPUT INSERTED.ID
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?);
        '''
        with pyodbc.connect(self.conn_str) as conn:
            cursor = conn.cursor()
            cursor.execute(query, values)
            inserted_id = cursor.fetchone()[0]
            conn.commit()
            return inserted_id

    def update(self, values):
        query = '''
            UPDATE Person
            SET [FirstName]=?, [LastName]=?, [Birthdate]=?, [NationalCode]=?, [Gender]=?,
                [Address]=?, [Mobile]=?, [EducationID]=?, [Photo]=?
            WHERE [ID]=?;
        '''
        with pyodbc.connect(self.conn_str) as conn:
            cursor = conn.cursor()
            cursor.execute(query, values)
            conn.commit()

    def delete(self, person_id):
        query = "DELETE FROM Person WHERE [ID]=?;"
        with pyodbc.connect(self.conn_str) as conn:
            cursor = conn.cursor()
            cursor.execute(query, (person_id,))
            conn.commit()