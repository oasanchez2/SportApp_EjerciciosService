from src.commands.create_ejercicio import CreateUser
from src.session import Session, engine
from src.models.model import Base
from src.models.ejercicio import User
from src.errors.errors import UserAlreadyExists
from src.errors.errors import IncompleteParams

class TestCreateUser():
  def setup_method(self):
    Base.metadata.create_all(engine)
    self.session = Session()

  def test_create_user_missing_field(self):
    try:
      CreateUser({}).execute()

      assert False
    except IncompleteParams:
      users = self.session.query(User).all()
      assert len(users) == 0

  def test_create_existing_username(self):
    first_data = {
        'username': 'william',
        'email': 'william@gmail.com',
        'password': '123456',
        'role':'candidato'
    }
    CreateUser(first_data).execute()
    try:
      second_data = {
        'username': 'william',
        'email': 'other_william@gmail.com',
        'password': '123456',
        'role':'candidato'
      }

      CreateUser(second_data).execute()

      assert False
    except UserAlreadyExists:
      users = self.session.query(User).all()
      assert len(users) == 1

  def test_create_existing_email(self):
    first_data = {
        'username': 'william',
        'email': 'william@gmail.com',
        'password': '123456',
        'role':'candidato'
    }
    CreateUser(first_data).execute()
    try:
      second_data = {
        'username': 'other_william',
        'email': 'william@gmail.com',
        'password': '123456',
        'role':'candidato'
      }

      CreateUser(second_data).execute()

      assert False
    except UserAlreadyExists:
      users = self.session.query(User).all()
      assert len(users) == 1

  def test_create_user(self):
    data = {
      'username': 'william',
      'email': 'william@gmail.com',
      'password': '123456',
      'role':'candidato'
    }
    user = CreateUser(data).execute()

    assert user['username'] == data['username']
    assert user['email'] == data['email']

    users = self.session.query(User).all()
    assert len(users) == 1
  
  def teardown_method(self):
    self.session.close()
    Base.metadata.drop_all(bind=engine)