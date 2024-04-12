import os 


class Config(object):
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URI", "sqlite:///db.sqlite3")
    SECRET_KEY = os.getenv("SECRET_KEY", "MY_SECRET_KEY")
    
    print(SQLALCHEMY_DATABASE_URI)