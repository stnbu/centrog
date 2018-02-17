"""
The Documentation
=================

This project is just getting off the ground, but I wanted to let folks know how to use it.

If You Use Goat
---------------


.. code::


That's it!! Your logs will be available here: http://10.20.68.188/

Figure out your syslog tag (a.k.a. "run name"), enter it in the `Syslog tag` texts box and click `Search`. Enjoy!

If your situation is more complicated or just need help, `go here <https://github.com/stnbu/centrog>`_

More
----


Contributions, collaborations welcome!

The `production server <http://10.20.68.188/>`_ really is "production" in the sense that I will try very hard not to
break it and maximize uptime. **HOWEVER** the IP address will change when it moves to its dedicated VM and also there
will be a memorable DNS name for it (suggestions welcome) hopefully soon.


lots of missing documentation content goes here...
--------------------------------------------------

blah blah blah


Setting up the Server
---------------------

Setting up the server is hard and is beyond the scope of this document. But since in practice someone might need to set
one up I will *temporarily* be hosting the stripped-down conf files related to the setup. Note that I used *only*
ubuntu packages and tried to do everything the Debian Way. I've stripped out all comments and whitespace from the config
files, these are provided only to be used as a hint, as they came from a working server.

Plopping these on a host is *not* the right thing to do.

Magical incantation to update server_config files:

.. code:: bash

    rm -rf /tmp/.foo
    mkdir -p /tmp/.foo && tar -C / -cf - etc/uwsgi/apps-available/centrog.ini etc/nginx/sites-available/default etc/default/uwsgi etc/rsyslog.d/pgsql.conf etc/postgresql/9.5/main/postgresql.conf etc/postgresql/9.5/main/pg_hba.conf etc/rsyslog.conf etc/dbconfig-common/rsyslog-pgsql.conf | tar -C /pyweb/centrog/production/server_config -xf -
    chown -R pyweb:pyweb /pyweb/centrog/production/server_config
    find /pyweb/centrog/production/server_config/ -type f -exec sed -r -i 's/#.*//;/^\s*(#|$)/d;/^[ \t]*$/d;s/[ \t]*$//' "{}" \;

The results can be found in the
`server_config/` folder.
"""

from base import *
