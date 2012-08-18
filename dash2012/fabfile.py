#encoding: utf-8
from fabric.api import run, settings, cd, env

env.use_ssh_config = True
env.ssh_config_path = '~/.ssh/config'


def deploy():
    with settings(host_string='dash.daltonmatos.com'):
        with cd("/var/mongrel2/apps/djangodash2012.daltonmatos.com"):
            with cd("app/djangodash2012/"):
                run("git reset --hard")
                run("git pull origin master")
            run("wsgid restart")
