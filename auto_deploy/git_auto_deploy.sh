cd /home/projectshroud
git checkout site
git reset --hard HEAD
git pull
while getopts ":ypfb" opt
do
    case $opt in
        f)
        echo "Building frontend"
        (cd frontend; yarn build)
        ;;
        b)
        echo "Migrating backend"
        #source /home/pyweb/bin/activate
        #python manage.py makemigrations
        #python manage.py migrate
        #deactivate
        ;;
        y)
        echo "Installing frontend dependencies and building"
        #(cd frontend; yarn install; yarn build)
        ;;
        p)
        echo "Installing python dependencies"
        #source /home/pyweb/bin/activate
        #pip install -r requirements.pip
        #deactivate
        ;;
    esac
done

uwsgi --reload projectshroud.pid

