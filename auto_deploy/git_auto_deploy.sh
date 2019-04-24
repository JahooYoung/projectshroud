cd /home/projectshroud
git checkout site
git reset --hard HEAD
git pull
while getopts ":f:b:" opt
do
    case $opt in
        f)
        if [ {$OPTARG}x = 'build'x ]; then
            echo "Building frontend"
            (cd frontend; yarn build)
        elif [ {$OPTARG}x = 'install'x ]; then
            echo "Installing frontend dependencies and building"
            (cd frontend; yarn install; yarn build)
        fi
        ;;
        b)
        if [ {$OPTARG}x = 'migrate'x ]; then
            echo "Migrating backend"
            source /home/pyweb/bin/activate
            python manage.py makemigrations
            python manage.py migrate
            deactivate
        fi
        ;;
    esac
done

uwsgi --reload projectshroud.pid

