import click, sys
from models import db, User,Todo
from app import app
from sqlalchemy.exc import IntegrityError


@app.cli.command("init", help="Creates and initializes the database")
def initialize():
  db.drop_all()
  db.init_app(app)
  db.create_all()
  bob = User('bob', 'bob@mail.com', 'bobpass')
  bob.todos.append(Todo("Car wash"))
  db.session.add(bob)
  db.session.commit()
  print(bob)
  print('database intialized')

@app.cli.command("get-user", help="this returns the username")
@click.argument('username', default='bob')
def get_user(username):
  bob = User.query.filter_by(username=username).first()
  if not bob:
    print(f'{username} not found')
    return
  print(bob)

@app.cli.command("get-users", help="returns all the users that have been created")
def get_users():
  users = User.query.all()
  print(users)

@app.cli.command('change-email',help="changes the current user email")
@click.argument('username', default="bob")
@click.argument('email', default= "bob@mail.com")
def change_mail(username,email):
  bob = User.query.filter_by(username=username).first()
  if not bob:
    print(f'{username} does not exist in Database')
  bob.email = email
  db.session.add(bob)
  db.session.commit()
  print(bob)

@app.cli.command("create-user",help="created a new user to the database")
@click.argument("username", default= "bob")
@click.argument('email', default = 'bob@mail.com')
@click.argument('password', default= 'bobpass')
def create_user(username,email,password):
  newuser = User(username,email,password)
  try:
    db.session.add(newuser)
    db.session.commit()
  except IntegrityError as e:
    db.session.rollback()
    print('User already taken try another one')
  else:
    print("New user created")

@app.cli.command("delete-user", help="delete the giving username from the db")
@click.argument("username", default='bob')
def delete_user(username):
  user = User.query.filter_by(username=username).first()
  if not user:
    print("User is not found")
    return
  else:
    db.session.delete(user)
    db.session.commit()
    print(f'{username} deleted')
@app.cli.command("get-todos",help = "this gets the user to do list")
@click.argument("username", default = "bob")
def get_user_todos(username):
  user = User.query.filter_by(username=username).first()
  if not user:
    print(f'{username} does not exist in DB')
    return
  else:
    print(user.todos)

@app.cli.command("add-todo")
@click.argument('username',default = "bob")
@click.argument("text", default = "Wash wears")
def add_task(username,text):
  user = User.query.filter_by(username=username).first()
  if not user:
    print(f'{username} does not exist')
    return
  else:
    new_task = Todo(text)
    user.todos.append(new_task)
    db.session.add(user)
    db.session.commit()
    print(f'{text} was added')

@app.cli.command('toggle-todo')
@click.argument('username', default='bob')
@click.argument('todo_id', default=1)
def toggle_todo_command(todo_id, username):
  user = User.query.filter_by(username=username).first()
  if not user:
    print(f'{username} not found!')
    return

  todo = Todo.query.filter_by(id=todo_id, user_id=user.id).first()
  if not todo:
    print(f'{username} has no todo id {todo_id}')

  todo.toggle()
  print(f'{todo.text} is {"done" if todo.done else "not done"}!')

@click.argument('username', default='bob')
@click.argument('todo_id', default=1)
@click.argument('category', default='chores')
@app.cli.command('add-category', help="Adds a category to a todo")
def add_todo_category_command(username, todo_id, category):
  user = User.query.filter_by(username=username).first()
  if not user:
    print(f'{username} not found!')
    return

  res = user.add_todo_category(todo_id, category)
  if not res:
    print(f'{username} has no todo id {todo_id}')
    return

  print('Category added!')