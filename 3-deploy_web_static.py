#!/usr/bin/python3
"""Fabric script for full deployment."""
from fabric.api import env, local, run
from datetime import datetime
import os

env.hosts = ['<IP web-01>', 'IP web-02']


def do_pack():
    """Generate a .tgz archive from the contents of the web_static folder."""
    try:
        current_time = datetime.now().strftime("%Y%m%d%H%M%S")
        archive_path = "versions/web_static_{}.tgz".format(current_time)
        local("mkdir -p versions")
        local("tar -cvzf {} web_static".format(archive_path))
        print("web_static packed: {} -> {}Bytes".format(archive_path, os.path.getsize(archive_path)))
        return archive_path
    except Exception as e:
        return None


def do_deploy(archive_path):
    """Distribute an archive to web servers."""
    # The implementation of do_deploy remains the same as in the previous response.


def deploy():
    """Create and distribute an archive to web servers."""
    archive_path = do_pack()
    if archive_path:
        return do_deploy(archive_path)
    else:
        return False


if __name__ == "__main__":
    deploy()
