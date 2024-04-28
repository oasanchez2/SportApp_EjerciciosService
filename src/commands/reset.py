from .base_command import BaseCommannd
from ..dynamodb_ejercicio import DynamoDbEjercicio

class Reset(BaseCommannd):  
  def execute(self):
    DynamoDbEjercicio().deleteTable()
    DynamoDbEjercicio().create_table()