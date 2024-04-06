from marshmallow import  Schema, fields
from sqlalchemy import Column, String, Boolean
from .model import Model, Base
from datetime import datetime, timedelta

class Exercise(Model, Base):
  __tablename__ = 'exercises'

  nombre = Column(String)
  estado = Column(Boolean)
  url_imagen = Column(String)

  def __init__(self, nombre, estado, url_imagen):
    Model.__init__(self)
    self.nombre = nombre
    self.estado = estado
    self.url_imagen = url_imagen
    
class ExerciseSchema(Schema):
  id = fields.Number()
  nombre = fields.Str()
  estado = fields.Bool()
  url_imagen = fields.Str()
  expireAt = fields.DateTime()
  createdAt = fields.DateTime()
 

class ExerciseJsonSchema(Schema):
  id = fields.Number()
  nombre = fields.Str()
  estado = fields.Bool()
  url_imagen = fields.Str()
  expireAt = fields.DateTime()
  createdAt = fields.DateTime()
  
  
