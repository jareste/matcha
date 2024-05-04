from flask import Flask
import os
from srcs import create_app
# from srcs.database import db

app = create_app()
# app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')

# db.init_app(app)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)