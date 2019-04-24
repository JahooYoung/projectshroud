cd /home/projectshroud
git checkout site
git reset --hard HEAD
git pull
if [ $1x = "yarn"x ]; then
    echo "Building frontend"
    (cd frontend; yarn build)
fi
uwsgi --reload projectshroud.pid

