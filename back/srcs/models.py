import sqlite3
import csv
from werkzeug.security import generate_password_hash
import random

import hashlib

def hash_to_db(name):
    hash_object = hashlib.sha256()

    hash_object.update(name.encode())

    hash_hex = hash_object.hexdigest()

    return hash_hex

class Field:
    def __init__(self, field_type, primary_key=False, autoincrement=False, default=None):
        self.type = field_type
        self.primary_key = primary_key
        self.autoincrement = autoincrement
        self.default = default

class BaseModel:
    id = Field('INTEGER', primary_key=True, autoincrement=True)
    
    def __init__(self, **kwargs):
        self.connection = sqlite3.connect('database.db')
        self.cursor = self.connection.cursor()
        self.table_name = self.__class__.__name__.lower()
        self.fields = {name: field for name, field in self.__class__.__dict__.items() if isinstance(field, Field)}
        self.create_table()
        
        for key, value in kwargs.items():
            setattr(self, key, value)

    def create_table(self):
        fields_str = ', '.join(f'{name} {field.type} PRIMARY KEY AUTOINCREMENT' if field.primary_key and field.autoincrement else f'{name} {field.type}' for name, field in self.fields.items())
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
        
        rows = self.cursor.fetchall()
        return [self._instantiate_from_row(row) for row in rows]

    def update(self, updates, conditions):
        updates_str = ', '.join(f'{field} = ?' for field in updates.keys())
        conditions_str = ' AND '.join(f'{field} = ?' for field in conditions.keys())
        values = tuple(list(updates.values()) + list(conditions.values()))
        self.cursor.execute(f'UPDATE {self.table_name} SET {updates_str} WHERE {conditions_str}', values)
        self.connection.commit()

    def _instantiate_from_row(self, row):
        obj = self.__class__()
        for idx, (name, field) in enumerate(self.fields.items()):
            setattr(obj, name, row[idx])
        return obj

    def get_fields(self):
        self.cursor.execute(f'PRAGMA table_info({self.table_name})')
        return self.cursor.fetchall()
    
    def select_all(self):
        self.cursor.execute(f'SELECT * FROM {self.table_name}')
        rows = self.cursor.fetchall()
        return [self._instantiate_from_row(row) for row in rows]

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
    id = Field('INTEGER', primary_key=True, autoincrement=True)
    user_id = Field('INTEGER')
    url = Field('TEXT')

class User(BaseModel):
    id = Field('INTEGER', primary_key=True, autoincrement=True)
    username = Field('TEXT')
    email = Field('TEXT')
    password = Field('TEXT')
    photo = Field('TEXT', default='')
    jwt = Field('TEXT', default='')
    likes = Field('TEXT', default='')
    matches = Field('TEXT', default='')
    description = Field('TEXT', default='')

    # Used when both users are in each other likes
    def add_match(self, target_id):
        matches = self.matches.split(',') if self.matches else []
        if target_id not in matches:
            matches.append(target_id)
            self.update({'matches': ','.join(matches)}, {'id': self.id})

    def add_like(self, target_id):
        return True

    def check_match(self, target_id):
        self.add_match(target_id)
        other_user = User().select(id=target_id)[0]
        if str(self.id) in other_user.matches.split(','):
            return True  # It's a match!
        return False
    
    def select_random(self):
        self.cursor.execute(f'SELECT * FROM {self.table_name}')
        rows = self.cursor.fetchall()
        if rows:
            return self._instantiate_from_row(random.choice(rows))
        else:
            return None




# class Field:
#     def __init__(self, field_type, primary_key=False, autoincrement=False, default=None):
#         self.type = field_type
#         self.primary_key = primary_key
#         self.autoincrement = autoincrement
#         self.default = default

# class BaseModel:
#     id = Field('INTEGER', primary_key=True, autoincrement=True)
    
#     def __init__(self, **kwargs):
#         self.connection = sqlite3.connect('database.db')
#         self.cursor = self.connection.cursor()
#         self.table_name = self.__class__.__name__.lower()
#         self.fields = {name: field for name, field in self.__class__.__dict__.items() if isinstance(field, Field)}
#         self.create_table()
        
#         for key, value in kwargs.items():
#             setattr(self, key, value)

#     def create_table(self):
#         fields_str = ', '.join(f'{name} {field.type} PRIMARY KEY AUTOINCREMENT' if field.primary_key and field.autoincrement else f'{name} {field.type}' for name, field in self.fields.items())
#         self.cursor.execute(f'CREATE TABLE IF NOT EXISTS {self.table_name} ({fields_str})')
#         self.connection.commit()

#     def insert(self, **kwargs):
#         fields_str = ', '.join(kwargs.keys())
#         values_str = ', '.join('?' for _ in kwargs.values())
#         values = tuple(kwargs.values())
#         self.cursor.execute(f'INSERT INTO {self.table_name} ({fields_str}) VALUES ({values_str})', values)
#         self.connection.commit()

#     def select(self, **conditions):
#         if conditions:
#             fields = conditions.keys()
#             values = tuple(conditions.values())
#             conditions_str = ' AND '.join(f'{field} = ?' for field in fields)
#             self.cursor.execute(f'SELECT * FROM {self.table_name} WHERE {conditions_str}', values)
#         else:
#             self.cursor.execute(f'SELECT * FROM {self.table_name}')
        
#         rows = self.cursor.fetchall()
#         return [self._instantiate_from_row(row) for row in rows]

#     def update(self, updates, conditions):
#         updates_str = ', '.join(f'{field} = ?' for field in updates.keys())
#         conditions_str = ' AND '.join(f'{field} = ?' for field in conditions.keys())
#         values = tuple(list(updates.values()) + list(conditions.values()))
#         self.cursor.execute(f'UPDATE {self.table_name} SET {updates_str} WHERE {conditions_str}', values)
#         self.connection.commit()

#     def _instantiate_from_row(self, row):
#         obj = self.__class__()
#         for idx, (name, field) in enumerate(self.fields.items()):
#             setattr(obj, name, row[idx])
#         return obj

#     def get_fields(self):
#         self.cursor.execute(f'PRAGMA table_info({self.table_name})')
#         return self.cursor.fetchall()
    
#     def select_all(self):
#         self.cursor.execute(f'SELECT * FROM {self.table_name}')
#         return self.cursor.fetchall()

#     def add_column(self, column_name, column_type):
#         self.cursor.execute(f'ALTER TABLE {self.table_name} ADD COLUMN {column_name} {column_type}')
#         self.connection.commit()
    
#     def delete(self, **conditions):
#         if conditions:
#             fields = conditions.keys()
#             values = tuple(conditions.values())
#             conditions_str = ' AND '.join(f'{field} = ?' for field in fields)
#             self.cursor.execute(f'DELETE FROM {self.table_name} WHERE {conditions_str}', values)
#             self.connection.commit()
#         else:
#             raise ValueError("No conditions provided for delete operation")



# class Photo(BaseModel):
#     id = Field('INTEGER', primary_key=True, autoincrement=True)
#     user_id = Field('INTEGER')
#     url = Field('TEXT')

# class User(BaseModel):
#     id = Field('INTEGER', primary_key=True, autoincrement=True)
#     username = Field('TEXT')
#     email = Field('TEXT')
#     password = Field('TEXT')
#     photo = Field('TEXT', default='')
#     jwt = Field('TEXT', default='')
#     matches = Field('TEXT', default='')

#     def add_match(self, match_id):
#         matches = self.matches.split(',') if self.matches else []
#         if match_id not in matches:
#             matches.append(match_id)
#             self.update({'matches': ','.join(matches)}, {'id': self.id})


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

# insert_users_from_csv('users.csv')

