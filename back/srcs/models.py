import sqlite3
import csv
from werkzeug.security import generate_password_hash
import random
from faker import Faker

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
    first_name = Field('TEXT')
    last_name = Field('TEXT')
    email = Field('TEXT')
    password = Field('TEXT')
    photo = Field('TEXT', default='')
    jwt = Field('TEXT', default='')
    likes = Field('TEXT', default='')
    dislikes = Field('TEXT', default='')
    matches = Field('TEXT', default='')
    description = Field('TEXT', default='')
    tags = Field('TEXT', default='')
    completed = Field('TEXT', default='false')
    enabled = Field('TEXT', default='false')
    gender = Field('TEXT', default='no specified')
    preference = Field('TEXT', default='no specified')
    age = Field('INTEGER')
    age_min = Field('INTEGER', default=18)
    age_max = Field('INTEGER', default=120)
    fame = Field('INTEGER', default=1000)
    location = Field('TEXT', default='')
    range = Field('INTEGER', default=25)

    # Predefined tags
    VALID_TAGS = {'#sport', '#movies', '#series', '#gym', '#pets', '#cats', '#coding', '#food',
        '#party', '#videogames'}
    
    VALID_GENDERS = {'men', 'woman', 'no specified'}

    # Validate tags against predefined list
    @staticmethod
    def validate_tags(tags):
        return all(tag in User.VALID_TAGS for tag in tags)

    def recommend_users(self):

        print('self.preference:', self.preference)
        conditions = {
            'enabled': 'true',
            'completed': 'true',
            'preference': self.gender,
            'gender': self.preference,
        }
        all_users = self.select(**conditions)
        
        all_users.sort(key=lambda user: user.fame, reverse=True)

        likes = self.likes.split(',') if self.likes else []
        dislikes = self.dislikes.split(',') if self.dislikes else []
        matches = self.matches.split(',') if self.matches else []

        recommended_users = []
        for user in all_users:
            if user.id == self.id:
                continue

            if str(user.id) in likes or str(user.id) in dislikes or str(user.id) in matches:
                continue

            ##
            if len(recommended_users) >= 10:
                break

            ##
            if user.age >= self.age_min and user.age <= self.age_max:
                user_tags = set(user.tags.split(','))
                self_tags = set(self.tags.split(','))
                
                if user_tags & self_tags:
                    recommended_users.append(user)
        
        return recommended_users


    def add_tags(self, tags):
        if not self.validate_tags(tags):
            raise ValueError("Invalid tags provided.")
        self.tags = ','.join(tags)
        self.update({'tags': self.tags}, {'id': self.id})

    def get_tags(self):
        return self.tags.split(',')

    def common_tags(self, other_user):
        my_tags = set(self.get_tags())
        other_tags = set(other_user.get_tags())
        return my_tags.intersection(other_tags)


    # Used when both users are in each other likes
    def add_match(self, target_id):
        print('target_id:', target_id)
        if not target_id:
            return False

        target = User().select(id=target_id)[0]
        target_likes = target.likes.split(',') if target.likes else []

        if str(self.id) not in target_likes:
            return False

        if str(target_id) in self.matches.split(',') if self.matches else []:
            return True

        matches = self.matches.split(',') if self.matches else []

        if str(target_id) not in matches:
            matches.append(str(target_id))
            target_matches = target.matches.split(',') if target.matches else []
            target_matches.append(str(self.id))
            target.update({'matches': ','.join(target_matches)}, {'id': target.id})
            self.update({'matches': ','.join(matches)}, {'id': self.id})
            return True
        return True


    def add_dislike(self, target_id):
        dislikes = self.dislikes.split(',') if self.dislikes else []
        
        likes = self.likes.split(',') if self.likes else []
        if str(target_id) in likes:
            likes.remove(str(target_id))
            updated_likes = ','.join(likes)
            self.update({'likes': updated_likes}, {'id': self.id})

        matches = self.matches.split(',') if self.matches else []
        if str(target_id) in matches:
            matches.remove(str(target_id))
            updated_matches = ','.join(matches)
            self.update({'matches': updated_matches}, {'id': self.id})

        if str(target_id) not in dislikes:
            dislikes.append(str(target_id))
            print('dislikesBefore::::::::::::::', self.dislikes)
            updated_dislikes = ','.join(dislikes)
            self.update({'dislikes': updated_dislikes}, {'id': self.id})
            self.dislikes = updated_dislikes
            print('dislikesAfter::::::::::::::', self.dislikes)
            return True
        
        return False

    def add_like(self, target_id):
        print('target_id333:', target_id)
        likes = self.likes.split(',') if self.likes else []
        
        likes = [like for like in likes if like]
        dislikes = self.dislikes.split(',') if self.dislikes else []

        print('updated_likes:', self.likes)
        print('id:', self.id)
        if str(target_id) in likes:
            return False
        
        if str(target_id) in dislikes:
            dislikes.remove(str(target_id))
            updated_dislikes = ','.join(dislikes)
            self.update({'dislikes': updated_dislikes}, {'id': self.id})

        likes.append(str(target_id))
        
        updated_likes = ','.join(likes)
        
        self.update({'likes': updated_likes}, {'id': self.id})
        print('updated_likes:', self.likes)
        print('id:', self.id)
        self.add_match(target_id)
        if self.add_match(target_id):
            return True

        return False


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

#DEBUG
# Generate and insert random users
fake = Faker()
user_model = User()

def generate_random_tags():
    tags = list(User.VALID_TAGS)
    return ','.join(random.sample(tags, k=2))

def generate_random_user(index):
    username = f'{fake.user_name()}{index}'
    first_name = fake.first_name()
    last_name = fake.last_name()
    email = fake.email()
    password = generate_password_hash('123456789')
    description = fake.text(max_nb_chars=random.randint(5, 420))
    age = random.randint(18, 85)
    age_min = random.randint(18, age)
    age_max = random.randint(age, 85)
    gender = random.choice(list(User.VALID_GENDERS))
    preference = random.choice(list(User.VALID_GENDERS))
    tags = generate_random_tags()
    location = f'{random.uniform(41.3, 41.5)},{random.uniform(2.0, 2.2)}' # Around Barcelona
    range_ = random.randint(0, 500)
    fame = random.randint(0, 5569)

    return {
        'username': username,
        'first_name': first_name,
        'last_name': last_name,
        'email': email,
        'password': password,
        'description': description,
        'age': age,
        'age_min': age_min,
        'age_max': age_max,
        'gender': gender,
        'preference': preference,
        'tags': tags,
        'photo': 'default.png',
        'location': location,
        'range': range_,
        'enabled': 'true',
        'completed': 'true',
        'fame': fame
    }

def insert_random_users(count=500):
    for i in range(count):
        user_data = generate_random_user(i + 1)
        user_model.insert(**user_data)
        print(f'Inserted user {i + 1}/{count}')

# insert_random_users()



