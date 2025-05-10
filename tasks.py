from invoke import task
from src.ui.main_login_view import open_login_view
from src.initialize_database import initialize_database

@task
def start(ctx):
    open_login_view()

@task
def build(ctx):  
    initialize_database()
    print("Database initialized")

@task
def lint(c):
    c.run("pylint src/models src/services src/repositories --rcfile=.pylintrc")

@task
def test(c):
    c.run("coverage run --source=src -m unittest discover -s src/tests")

@task
def coverage_report(c):
    c.run("coverage html")
