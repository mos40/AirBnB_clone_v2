#!/usr/bin/python3
"""
Fabric script (based on the file 1-pack_web_static.py) that distributes an
archive to your web servers, using the function do_deploy
"""

from fabric.api import *
from os import path

env.hosts = ['<IP web-01>', 'IP web-02']
env.user = 'ubuntu'


def do_deploy(archive_path):
    """
    Distributes an archive to your web servers
    """

    if not path.exists(archive_path):
        return False

    try:
        # Upload the archive to the /tmp/ directory of the web server
        put(archive_path, "/tmp/")

        # Uncompress the archive to the folder
        # /data/web_static/releases/<archive filename without extension>
        filename = archive_path.split('/')[-1]
        foldername = filename.split('.')[0]
        run("mkdir -p /data/web_static/releases/{}/".format(foldername))
        run("tar -xzf /tmp/{} -C /data/web_static/releases/{}/"
            .format(filename, foldername))

        # Delete the archive from the web server
        run("rm /tmp/{}".format(filename))

        # Move the contents of the uncompressed folder to its parent directory
        run("mv /data/web_static/releases/{}/web_static/* "
            "/data/web_static/releases/{}/"
            .format(foldername, foldername))

        # Delete the symbolic link /data/web_static/current from the web server
        run("rm -rf /data/web_static/current")

        # Create a new symbolic link
        # /data/web_static/current on the web server
        run("ln -s /data/web_static/releases/{}/ /data/web_static/current"
            .format(foldername))

        print("New version deployed!")
        return True
    except Exception as e:
        return False
