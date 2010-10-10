#!/bin/sh

USER=www-data
NAME="placeholder"
CONFDIR="/home/mikewest/public_html/placeholder.mikewest.org/env/flask-pyplaceholder"
VENV_ACTIVATION=". ../bin/activate"
RETVAL=0
PID="/tmp/gunicorn_${NAME}.pid"
GUNICORN_RUN="../bin/gunicorn -w 4 -D --user www-data --pid ${PID} generator:app"

. /lib/lsb/init-functions

start()
{
    echo "Starting $NAME"
    cd $CONFDIR;
    su -c "$VENV_ACTIVATION; $GUNICORN_RUN" $USER && echo "OK" || echo "failed";
}
stop()
{
    echo "Stopping $NAME"
    kill -QUIT `cat $PID` && echo "OK" || echo "failed";
}

reload()
{
    echo "Reloading $NAME:"
    if [ -f $PID ]
    then kill -HUP `cat $PID` && echo "OK" || echo "failed";
    fi
}

case "$1" in
    start)
        start
        ;;
    stop)
        stop
        ;;
    restart)
        reload
        ;;
    reload)
        reload
        ;;
    force-reload)
        stop && start
        ;;
    *)
        echo $"Usage: $0 {start|stop|restart}"
        RETVAL=1
esac
exit $RETVAL
