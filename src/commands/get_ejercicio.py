from .base_command import BaseCommannd
from ..errors.errors import Unauthorized, InvalidParams, ExerciseNotFoundError
from ..dynamodb_ejercicio import DynamoDbEjercicio

class GetEjercicio (BaseCommannd):
  def __init__(self, exercise_id):
    if exercise_id and exercise_id.strip():
      self.exercise_id = exercise_id
    else:
      raise InvalidParams()
  
  def execute(self):
    
    result  = DynamoDbEjercicio().get_item(self.exercise_id)
    if result is None:
      raise ExerciseNotFoundError()
    
    return result