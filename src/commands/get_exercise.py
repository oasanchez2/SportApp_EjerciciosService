from .base_command import BaseCommannd
from ..models.exercise import Exercise, ExerciseSchema, ExerciseJsonSchema
from ..session import Session
from ..errors.errors import Unauthorized, InvalidParams, ExerciseNotFoundError

class GetExercise (BaseCommannd):
  def __init__(self, exercise_id):
    if self.is_integer(exercise_id):
      self.exercise_id = int(exercise_id)
    elif self.is_float(exercise_id):
      self.exercise_id = int(float(exercise_id))
    else:
      raise InvalidParams()
  
  def execute(self):
    session = Session()

    if len(session.query(Exercise).filter_by(id=self.exercise_id).all()) <= 0:
      session.close()
      raise ExerciseNotFoundError()
    
    exercise = session.query(Exercise).filter_by(id=self.exercise_id).one()
    schema = ExerciseSchema()
    exercise = schema.dump(exercise)

    session.close()

    return exercise
  
      
  def is_integer(self, string):
    try:
      int(string)
      return True
    except:
      return False

  def is_float(self, string):
    try:
      float(string)
      return True
    except:
      return False