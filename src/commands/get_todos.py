from .base_command import BaseCommannd
from ..errors.errors import Unauthorized, InvalidParams, ExerciseNotFoundError
from ..dynamodb_ejercicio import DynamoDbEjercicio

class GetTodos (BaseCommannd):
  def __init__(self):
    pass
  
  def execute(self):    
    result  = DynamoDbEjercicio().get_all()
    if result is None:
      raise ExerciseNotFoundError()
    
    return result
