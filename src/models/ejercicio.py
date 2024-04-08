from typing import Optional

class Ejercicio():

  def __init__(self, id_ejercicio: str, nombre: str, estado: bool, url_imagen: str):
    self.id_ejercicio = id_ejercicio
    self.nombre = nombre
    self.estado = estado
    self.url_imagen = url_imagen

  def to_dict(self):
        return {
            "id_ejercicio": self.id_ejercicio,
            "nombre": self.nombre,
            "estado": self.estado,
            "url_imagen": self.url_imagen
            
        }