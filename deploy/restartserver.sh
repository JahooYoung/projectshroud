sudo /usr/local/nginx/sbin/nginx -s reload
cd /home/projectshroud
uwsgi --reload projectshroud.pid
