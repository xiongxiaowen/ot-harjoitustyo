from invoke import task
from src.ui.main_login_view import open_login_view

@task
def start(ctx):
    open_login_view()


@task
def lint(c):
    c.run("pylint src/models src/services src/repositories --rcfile=.pylintrc")

@task
def coverage_report(c):
    c.run("coverage report")