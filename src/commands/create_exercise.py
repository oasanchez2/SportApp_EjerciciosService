from .base_command import BaseCommannd
from ..models.exercise import Exercise, ExerciseSchema,ExerciseJsonSchema
from ..session import Session
from ..errors.errors import IncompleteParams, InvalidNombreError, ExercisesAlreadyExists

class CreateExercises(BaseCommannd):
  def __init__(self, data):
    self.data = data
  
  def execute(self):
    try:
      posted_exercises = ExerciseSchema(
        only=('nombre', 'estado', 'url_imagen')
      ).load(self.data)
      print(posted_exercises)
      
      if not self.verificar_datos(posted_exercises["nombre"]):
         raise InvalidNombreError
      
      exercise = Exercise(**posted_exercises)
      session = Session()
      
      if self.exercise_exist(session, self.data['nombre']):
        session.close()
        raise ExercisesAlreadyExists()

      session.add(exercise)
      session.commit()

      new_exercise = ExerciseJsonSchema().dump(exercise)
      session.close()

      return new_exercise
        
    except TypeError as te:
      print("Error en el primer try:", str(te))
      raise IncompleteParams()
  
  def exercise_exist(self, session, nombre):
    return len(session.query(Exercise).filter_by(nombre=nombre).all()) > 0
  
  def verificar_datos(self,nombre):
    if nombre and nombre.strip():
        return True
    else:
        return False