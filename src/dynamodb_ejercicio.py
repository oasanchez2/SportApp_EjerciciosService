import boto3
import os
import json
from boto3.dynamodb.conditions import Key, Attr
from .models.ejercicio import Ejercicio
from botocore.exceptions import ClientError

class DynamoDbEjercicio():
    def __init__(self):
        # Crear una instancia de cliente DynamoDB
        self.dynamodb = boto3.client('dynamodb',
                                region_name='us-east-1',
                                aws_access_key_id= os.environ['AWS_ACCESS_KEY_ID'],
                                aws_secret_access_key= os.environ['AWS_SECRET_ACCESS_KEY'])
        self.table_name = 'ejercicios'

    # Funciones para interactuar con DynamoDB

    def create_table(self):
        if not self.tablaExits(self.table_name):

            self.dynamodb.create_table(
                    TableName=self.table_name,
                    AttributeDefinitions=[
                        {
                            'AttributeName': 'id_ejercicio',
                            'AttributeType': 'S',
                        }
                    ],
                    KeySchema=[
                        {
                            'AttributeName': 'id_ejercicio',
                            'KeyType': 'HASH'  # Clave de partición
                        }
                    ],        
                    BillingMode='PAY_PER_REQUEST'
                )
            
            # Espera hasta que la tabla exista
            self.dynamodb.get_waiter('table_exists').wait(TableName=self.table_name)
            print(f'Tabla {self.table_name} creada correctamente.')
        else:
            print(f"La tabla '{self.table_name}' ya existe.")

    def insert_item(self,ejercicio: Ejercicio):
        item = {
            "id_ejercicio": {'S':  ejercicio.id_ejercicio },
            'nombre': {'S': ejercicio.nombre },
            'estado': {'BOOL': ejercicio.estado },
            'url_imagen': {'S': ejercicio.url_imagen}
            # Puedes agregar más atributos según la definición de tu tabla
        }
        result = self.dynamodb.put_item(
            TableName=self.table_name,
            Item=item,
            ReturnConsumedCapacity='TOTAL'
        )
        print('Ítem insertado correctamente.')

    def get_item(self,id_ejercicio):
        key = {
            'id_ejercicio': {'S': str(id_ejercicio) }  # Clave de búsqueda
        }
        response = self.dynamodb.get_item(
            TableName=self.table_name,
            Key=key
        )
        item = response.get('Item')
        if not item:
            return None

        # Extrae los valores de cada campo
        id_ejercicio = item['id_ejercicio']['S']
        nombre = item['nombre']['S']
        estado = item['estado']['BOOL']
        url_imagen = item['url_imagen']['S']
        

        # Crea una instancia de la clase Entrenamiento
        ejercicio = Ejercicio(id_ejercicio,nombre, estado, url_imagen)

        # Serializa el objeto a JSON utilizando el método to_dict()
        json_ejercicio = ejercicio.to_dict()

        return json_ejercicio

    def get_Item_nombre(self,nombre):
        
        # Parámetros para la operación de escaneo
        parametros = {
            'TableName': self.table_name,
            'FilterExpression': '#nombre = :nombre',
            'ExpressionAttributeNames': {
                '#nombre': 'nombre'
            },
            'ExpressionAttributeValues': {
                ':nombre': {'S': nombre}
            }
        }
        
        # Realizar el escaneo
        response = self.dynamodb.scan(**parametros)
        print(response)
        # Obtener los items encontrados
        items = response.get('Items', [])
        if not items:
            return None
        
        # Procesar los items encontrados
        resultados = []
        for item in items:
            id_ejercicio = item['id_ejercicio']['S']
            nombre = item['nombre']['S']
            estado = item['estado']['BOOL']
            url_imagen = item['url_imagen']['S']
        

            ejercicio = Ejercicio(id_ejercicio,nombre, estado, url_imagen)
            resultados.append(ejercicio.to_dict())

        return resultados

    def get_all(self):
        # Escaneo de todos los elementos de la tabla
        response = self.dynamodb.scan(
            TableName=self.table_name
        )

        # Recuperar los items escaneados
        items = response['Items']
        if not items:
            return None
        
        # Si hay más resultados, seguir escaneando
        while 'LastEvaluatedKey' in response:
            response = self.dynamodb.scan(
                TableName=self.table_name,
                ExclusiveStartKey=response['LastEvaluatedKey']
            )
            items.extend(response['Items'])
        
        # Procesar los items encontrados
        resultados = []
        for item in items:
            id_ejercicio = item['id_ejercicio']['S']
            nombre = item['nombre']['S']
            estado = item['estado']['BOOL']
            url_imagen = item['url_imagen']['S']
        
            ejercicio = Ejercicio(id_ejercicio,nombre, estado, url_imagen)
            resultados.append(ejercicio.to_dict())
        
        return resultados

    def tablaExits(self,name):
        try:
            response = self.dynamodb.describe_table(TableName=name)
            print(response)
            return True
        except ClientError as err:
            print(f"Here's why: {err.response['Error']['Code']}: {err.response['Error']['Message']}")
            if err.response['Error']['Code'] == 'ResourceNotFoundException':
                return False

    def deleteTable(self):
        # Eliminar la tabla
        self.dynamodb.delete_table(TableName=self.table_name)

        # Esperar hasta que la tabla no exista
        self.dynamodb.get_waiter('table_not_exists').wait(TableName=self.table_name)