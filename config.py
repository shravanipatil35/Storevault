import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'super-secret-key-12345')
    
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:Shravani%4030@127.0.0.1/storevault"
    
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = True