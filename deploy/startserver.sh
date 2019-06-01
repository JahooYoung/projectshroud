sudo /usr/local/nginx/sbin/nginx
cd /home/projectshroud
# uwsgi --ini uwsgi.ini
supervisord -c ./deploy/supervisord.conf
