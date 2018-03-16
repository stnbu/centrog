"""
The Documentation
=================

This project is just getting off the ground, but I wanted to let folks know how to use it.

If You Use Goat
---------------

The changes required for remote logging are currently checked into `development` but will only be enabled if you're
doing a nimbus run. Output will include a line like this:

.. code::

    http://localhost/?syslogtag=XXXXXXXXXX.XX

The UI is fairly simple, feel free to play around.


More
----


Contributions, collaborations welcome!

Very simple and easy to adapt to any project using python, you must need to include a syslog "tag".


Setting up the Server
---------------------

Setting up the server is hard and is beyond the scope of this document. But since in practice someone might need to set
one up I will *temporarily* be hosting the stripped-down conf files related to the setup. Note that I used *only*
ubuntu packages and tried to do everything the Debian Way. I've stripped out all comments and whitespace from the config
files, these are provided only to be used as a hint, as they came from a working server.

Plopping these on a host is *not* the right thing to do.

Magical incantation to update server_config files...

.. code:: bash

    rm -rf /tmp/.foo
    mkdir -p /tmp/.foo && tar -C / -cf - etc/uwsgi/apps-available/centrog.ini etc/nginx/sites-available/default etc/default/uwsgi etc/rsyslog.d/pgsql.conf etc/postgresql/9.5/main/postgresql.conf etc/postgresql/9.5/main/pg_hba.conf etc/rsyslog.conf etc/dbconfig-common/rsyslog-pgsql.conf | tar -C /pyweb/centrog/production/server_config -xf -
    chown -R pyweb:pyweb /pyweb/centrog/production/server_config
    find /pyweb/centrog/production/server_config/ -type f -exec sed -r -i 's/#.*//;/^\s*(#|$)/d;/^[ \t]*$/d;s/[ \t]*$//' "{}" \;

The results can be found in the
`server_config/` folder.

How I create docs (the wrong way) as of now...

.. code:: bash

    python -c 'import centrog ; print centrog.__doc__' | \\
     rst2html | \\
     ssh mburr@10.20.68.95 'cat > ~/public_html/scratch/temporary_centrog_docs.html'
"""

from base import *
