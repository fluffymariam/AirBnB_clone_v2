#!/usr/bin/python3
"""Fabric script that generates a .tgz archive from the contents
   of the web_static folder.
"""

from fabric.api import local
from datetime import datetime
import os


def do_pack():
    """Generates a .tgz archive from the contents of the web_static folder."""
    try:
        now = datetime.utcnow()
        archive_name = "web_static_{}{}{}{}{}{}.tgz".format(
            now.year, now.month, now.day, now.hour, now.minute, now.second
        )
        archive_path = "versions/{}".format(archive_name)

        if not os.path.exists("versions"):
            local("mkdir -p versions")

        local("tar -cvzf {} web_static".format(archive_path))

        return archive_path
    except Exception as e:
        return None
