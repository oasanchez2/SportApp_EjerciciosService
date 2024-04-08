from .base_command import BaseCommannd
from .. import dynamodb_ejercicio

class Reset(BaseCommannd):  
  def execute(self):
    dynamodb_ejercicio.deleteTable()
    dynamodb_ejercicio.create_table()