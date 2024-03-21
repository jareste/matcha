import sqlite3

class Field:
    def __init__(self, field_type, default=None):
        self.type = field_type
        self.default = default

class BaseModel:
    def __init__(self, **kwargs):
        self.connection = sqlite3.connect('database.db')
        self.cursor = self.connection.cursor()
        self.table_name = self.__class__.__name__.lower()
        self.fields = {name: field for name, field in self.__class__.__dict__.items() if isinstance(field, Field)}
        self.create_table()

    def create_table(self):
        fields_str = ', '.join(f'{name} {field.type}' for name, field in self.fields.items())
        self.cursor.execute(f'CREATE TABLE IF NOT EXISTS {self.table_name} ({fields_str})')
        self.connection.commit()

    def insert(self, **kwargs):
        fields_str = ', '.join(kwargs.keys())
        values_str = ', '.join('?' for _ in kwargs.values())
        values = tuple(kwargs.values())
        self.cursor.execute(f'INSERT INTO {self.table_name} ({fields_str}) VALUES ({values_str})', values)
        self.connection.commit()

    def select(self, **conditions):
        if conditions:
            fields = conditions.keys()
            values = tuple(conditions.values())
            conditions_str = ' AND '.join(f'{field} = ?' for field in fields)
            self.cursor.execute(f'SELECT * FROM {self.table_name} WHERE {conditions_str}', values)
        else:
            self.cursor.execute(f'SELECT * FROM {self.table_name}')
        return self.cursor.fetchall()

    def update(self, updates, conditions):
        updates_str = ', '.join(f'{field} = ?' for field in updates.keys())
        conditions_str = ' AND '.join(f'{field} = ?' for field in conditions.keys())
        values = tuple(list(updates.values()) + list(conditions.values()))
        self.cursor.execute(f'UPDATE {self.table_name} SET {updates_str} WHERE {conditions_str}', values)
        self.connection.commit()

    def get_fields(self):
        self.cursor.execute(f'PRAGMA table_info({self.table_name})')
        return self.cursor.fetchall()
    
    def add_column(self, column_name, column_type):
        self.cursor.execute(f'ALTER TABLE {self.table_name} ADD COLUMN {column_name} {column_type}')
        self.connection.commit()

class User(BaseModel):
    username = Field('TEXT')
    email = Field('TEXT')
    password = Field('TEXT')
    jwt = Field('TEXT', default='')

# Usage
user = User()
# user.add_column('jwt', 'TEXT')
user.insert(username='test', email='test@test.com', password='password', jwt='')
print(user.select(username='test'))