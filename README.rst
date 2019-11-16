Program Description
===================

Clone and update all the Git repositories stored on a Gitea server. If
run periodically, it can maintain an updated collection of repositores
as a backup.

Usage
-----

This is the help from the command line::

    usage: saverepos.py [-h] [--basedir DIR] [--loglevel LEVEL] url

    Maintain an updated collection of the GIT repositories in a Gitea server.

    positional arguments:
      url                   URL of the Gitea server.

    optional arguments:
      -h, --help            show this help message and exit
      --basedir DIR, -d DIR
                            Base directory where the repositories will be held.
      --loglevel LEVEL, -l LEVEL
                            Logging level (DEBUG, INFO, WARNING, ERROR)

An example would be:

    $ saverepos -d ~/backup/gitrepos  http://giteasrv:3000

This will download the list of all the repositories from a Gitea server,
and clone or update them into the base directory to maintain a directory
structure as follows::

        basedir/
            user1/
                repo1
                repo2
                ...
            user2/
                repo3
                repo4
                ...
            ...

Installation
------------

Just use the provided ``setup.py`` utility::

    $ python3 setup.py install [--user]


License
-------
This software is released under the **MIT License**
