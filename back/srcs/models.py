import sqlite3
import csv
from werkzeug.security import generate_password_hash

import hashlib

def hash_to_db(name):
    hash_object = hashlib.sha256()

    hash_object.update(name.encode())

    hash_hex = hash_object.hexdigest()

    return hash_hex

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
    
    def select_all(self):
        self.cursor.execute(f'SELECT * FROM {self.table_name}')
        return self.cursor.fetchall()

    def add_column(self, column_name, column_type):
        self.cursor.execute(f'ALTER TABLE {self.table_name} ADD COLUMN {column_name} {column_type}')
        self.connection.commit()
    
    def delete(self, **conditions):
        if conditions:
            fields = conditions.keys()
            values = tuple(conditions.values())
            conditions_str = ' AND '.join(f'{field} = ?' for field in fields)
            self.cursor.execute(f'DELETE FROM {self.table_name} WHERE {conditions_str}', values)
            self.connection.commit()
        else:
            raise ValueError("No conditions provided for delete operation")



class Photo(BaseModel):
    user_id = Field('INTEGER')
    url = Field('TEXT')
    # To use::
    # To add a photo for a user
    # photo = Photo()
    # photo.insert(user_id=user_id, url='/path/to/photo.jpg')
    # # To get all photos for a user
    # photos = photo.select(user_id=user_id)

class User(BaseModel):
    username = Field('TEXT')
    email = Field('TEXT')
    password = Field('TEXT')
    jwt = Field('TEXT', default='')

def insert_users_from_csv(file_name):
    with open(file_name, 'r') as file:
        reader = csv.DictReader(file)
        user = User()
        for row in reader:
            existing_user = user.select(username=row['username'], email=row['email'])
            if not existing_user:
                hashed_password = generate_password_hash(row['password'])
                row['password'] = hashed_password
                user.insert(**row)

    all_users = user.select_all()
    for user in all_users:
        print(user)

insert_users_from_csv('users.csv')

