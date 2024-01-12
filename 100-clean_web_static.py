#!/usr/bin/python3
"""Fabric script for cleaning up outdated archives."""
from fabric.api import env, local, run
import os

env.hosts = ['<IP web-01>', '<IP web-02>']


def do_clean(number=0):
    """Delete outdated archives."""
    try:
        number = int(number)
        if number < 0:
            return
        number = number if number > 1 else 1
        local("ls -t versions | tail -n +{} | xargs -I {{}} rm versions/{{}}".format(number + 1))
        run("ls -t /data/web_static/releases | tail -n +{} | xargs -I {{}} rm -rf /data/web_static/releases/{{}}".format(number + 1))
    except Exception as e:
        pass


if __name__ == "__main__":
    do_clean()
