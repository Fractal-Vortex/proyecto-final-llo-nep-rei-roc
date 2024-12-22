from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, ForeignKey, Integer, String, Enum
from sqlalchemy.orm import relationship, declarative_base

db = SQLAlchemy()

class Users(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)

    def __repr__(self):
        return f'<Users {self.email}>'

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
        }
    
class Rutas(db.Model):
    __tablename__ = 'rutas'
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(120), unique=True, nullable=False)
    detalles = db.Column(db.JSON, nullable=True)
    usuario_id = db.Column(db.Integer, ForeignKey("users.id"), nullable=True) 
    category_id = db.Column(db.Integer, ForeignKey("categorias.id"), nullable=True)
    fecha_creada = db.Column(db.Date, nullable=False)
    fecha_inicio = db.Column(db.Date, nullable=False)


    user = relationship('Users', foreign_keys=[usuario_id], backref="rutas")
    categoria = relationship('Categorias', foreign_keys=[category_id], backref="rutas")

    def __repr__(self):
        return f'<Rutas {self.titulo}>'

    def serialize(self):
        return {
            "id": self.id,
            "titulo": self.titulo,
            "detalles": self.detalles,
            "usuario_id": self.usuario_id,
            "category_id": self.category_id,
            "fecha_creada": self.fecha_creada.isoformat() if self.fecha_creada else None,
            "fecha_inicio": self.fecha_inicio.isoformat() if self.fecha_inicio else None,
        }

class Categorias(db.Model):
    __tablename__ = 'categorias'
    id = db.Column(db.Integer, primary_key=True)
    categoria = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return f'<Categorias {self.categoria}>'

    def serialize(self):
        return {
            "id": self.id,
            "categoria": self.categoria,
        }
