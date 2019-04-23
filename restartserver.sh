sudo /usr/local/nginx/sbin/nginx -s reload
pkill -f uwsgi -9
uwsgi --ini uwsgi.ini
