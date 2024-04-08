import uuid
from .base_command import BaseCommannd
from ..models.ejercicio import Ejercicio
from ..errors.errors import IncompleteParams, InvalidNombreError, ExercisesAlreadyExists
from .. import dynamodb_ejercicio

class CreateEjercicio(BaseCommannd):
  def __init__(self, data):
    self.data = data
  
  def execute(self):
    try:
      posted_exercises = Ejercicio(str(uuid.uuid4()),self.data['nombre'],self.data['estado'],self.data['url_imagen'])
      print(posted_exercises)
      
      if not self.verificar_datos(self.data['nombre']):
         raise InvalidNombreError
      
      if self.exercise_exist(self.data['nombre']):
        raise ExercisesAlreadyExists()
      
      dynamodb_ejercicio.insert_item(posted_exercises)
      
      return posted_exercises.to_dict()
        
    except TypeError as te:
      print("Error en el primer try:", str(te))
      raise IncompleteParams()
  
  def exercise_exist(self, nombre):
    result = dynamodb_ejercicio.get_Item_nombre(nombre)
    if result is None:
      return False
    else:
      return True
  
  def verificar_datos(self,nombre):
    if nombre and nombre.strip():
        return True
    else:
        return False