#!/usr/bin/python3
"""Fabric script that deploys an archive to web servers."""
from fabric.api import env, run, put
from os.path import exists

env.hosts = ['<IP web-01>', 'IP web-02']


def do_deploy(archive_path):
    """Distributes an archive to web servers."""
    if not exists(archive_path):
        return False

    try:
        archive_name = archive_path.split("/")[-1]
        archive_without_ext = archive_name.split(".")[0]

        put(archive_path, "/tmp/{}".format(archive_name))
        run("mkdir -p /data/web_static/releases/{}/".format(archive_without_ext))
        run("tar -xzf /tmp/{} -C /data/web_static/releases/{}/"
            .format(archive_name, archive_without_ext))
        run("rm /tmp/{}".format(archive_name))
        run("mv /data/web_static/releases/{}/web_static/* /data/web_static/releases/{}/"
            .format(archive_without_ext, archive_without_ext))
        run("rm -rf /data/web_static/releases/{}/web_static"
            .format(archive_without_ext))
        run("rm -rf /data/web_static/current")
        run("ln -s /data/web_static/releases/{}/ /data/web_static/current"
            .format(archive_without_ext))

        print("New version deployed!")
        return True
    except Exception as e:
        return False
