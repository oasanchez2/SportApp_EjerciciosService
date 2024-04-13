from .base_command import BaseCommannd
from ..errors.errors import Unauthorized, InvalidParams, ExerciseNotFoundError
from .. import dynamodb_ejercicio

class GetTodos (BaseCommannd):
  def __init__(self):
    pass
  
  def execute(self):    
    result  = dynamodb_ejercicio.get_all()
    if result is None:
      raise ExerciseNotFoundError()
    
    return result
