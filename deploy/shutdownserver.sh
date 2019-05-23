sudo /usr/local/nginx/sbin/nginx -s quit
cd /home/projectshroud
uwsgi --stop projectshroud.pid
