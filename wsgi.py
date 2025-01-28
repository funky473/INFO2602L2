import click, sys
from models import db, User
from app import app


@app.cli.command("init", help="Creates and initializes the database")
def initialize():
  db.drop_all()
  db.init_app(app)
  db.create_all()
  bob = User('bob', 'bob@mail.com', 'bobpass')
  john = User('john', 'john@mail.com', 'johnpass')
  db.session.add(john)
  db.session.add(bob)
  db.session.commit()
  print(bob)
  print(john)
  #print('database initialized')
@app.cli.command("get-user", help="Create a user")
@click.argument('username', default='bob')
def getuser(username):
  bob = User.query.filter_by(username=username).first()
  if not bob:
    print("User ",username,"Not found in database")
    return
  print(bob)

@app.cli.command("get-users", help="get all users in the Database")
def getusers():
  all = User.query.all()
  print(all)

@app.cli.command("change-email",help="update the user email")
@click.argument("username",default="bob")
@click.argument("email",default="bob@mail.com")
def update_user(username,email):
  obb = User.query.filter_by(username=username).first()
  if not obb:
    print("User ",username,"Not found in database")
    return
  obb.email=email
  db.session.add(obb)
  db.session.commit()
  print(obb)

@app.cli.command("create-user",help="create a new user")
@click.argument("username",default="rick")
@click.argument("email",default="rick@mail.com")
@click.argument("password",default="rickpass")
def new_user(username,email,password):
  newuser=User(username,email,password)
  try:
    db.session.add(newuser)
    db.session.commit()
  except IntegrityError as e:
    db.session.rollback()
    print("Username already taking, try another")
  else:
    print(newuser)