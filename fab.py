from __future__ import with_statement
from fabric.api import *
from fabric.contrib.console import confirm
from __future__ import with_statement
from fabric.api import *
from contextlib import contextmanager as _contextmanager
from host import *

env.hosts = ['my_server']


env.hosts = []
env.user = 'deploy'
env.keyfile = ['$HOME/.ssh/deploy_rsa']
env.directory = '/path/to/virtualenvs/project'
env.activate = 'source /path/to/virtualenvs/project/bin/activate'

@_contextmanager
def virtualenv():
    with cd(env.directory):
        with prefix(env.activate):
            yield

def deploy():
    with virtualenv():
        run('pip freeze')

def test():
    with settings(warn_only=True):
        result = local('./manage.py test my_app', capture=True)
    if result.failed and not confirm("Tests failed. Continue anyway?"):
        abort("Aborting at user request.")

def commit():
    local("git add -p && git commit")

def push():
    local("git push")

def prepare_deploy():
    test()
    commit()
    push()

def deploy():
    code_dir = '/srv/django/myproject'
    with settings(warn_only=True):
        if run("test -d %s" % code_dir).failed:
            run("git clone user@vcshost:/path/to/repo/.git %s" % code_dir)
    with cd(code_dir):
        run("git pull")
        run("touch app.wsgi")
