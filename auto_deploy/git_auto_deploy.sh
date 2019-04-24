cd /home/projectshroud
git reset --hard HEAD
git pull
(cd frontend; yarn build)
uwsgi --reload projectshroud.pid

