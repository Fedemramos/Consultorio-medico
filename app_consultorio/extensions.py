from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

"""
archivo creado para soluciona el problema de  from app_consultorio import db
(ImportError: cannot import name 'db' from partially initialized module 
'app_consultorio' (most likely due to a circular import))

"""