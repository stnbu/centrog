"""

...lots of missing documentation content goes here...

Setting up the Server
---------------------

Setting up the server is hard and is beyond the scope of this document. But since in practice someone might need to set
one up I will *temporarally* be hosting the stripped-down conf files related to the setup. Note that I used *only*
ubuntu packages and tried to do everything the Debian Way. I've stripped out all comments and whitespace from the config
files, these are provided only to be used as a hint, as they came from a working server.

Plopping these on a host is *not* the right thing to do.

Magical incantation to update server_config files:

rm -rf /tmp/.foo && mkdir -p /tmp/.foo && tar -C / -cf - etc/uwsgi/apps-available/centrog.ini etc/nginx/sites-available/default etc/default/uwsgi etc/rsyslog.d/pgsql.conf etc/postgresql/9.5/main/postgresql.conf etc/postgresql/9.5/main/pg_hba.conf etc/rsyslog.conf etc/dbconfig-common/rsyslog-pgsql.conf | tar -C /pyweb/centrog/production/server_config -xf - && chown -R pyweb:pyweb /pyweb/centrog/production/server_config && find /pyweb/centrog/production/server_config/ -type f -exec sed -r -i 's/#.*//;/^\s*(#|$)/d;/^[ \t]*$/d;s/[ \t]*$//' "{}" \;

The results can be found in ``
"""

from base import *
