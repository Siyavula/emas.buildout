#! /bin/sh
### BEGIN INIT INFO
# Provides:		redis-emas-server
# Required-Start:	$syslog $remote_fs
# Required-Stop:	$syslog $remote_fs
# Should-Start:		$local_fs
# Should-Stop:		$local_fs
# Default-Start:	2 3 4 5
# Default-Stop:		0 1 6
# Short-Description:    emas redis-server - Persistent key-value db
# Description:		emas redis-server - Persistent key-value db for EMAS sites
### END INIT INFO

SRVUSER="zope"

# If file is a symlink, resolve it
SOURCE="${BASH_SOURCE[0]}"
if test -L "$SOURCE"; then
    SOURCE=$(readlink "$SOURCE")
fi
DIR="$(cd "$( dirname "$SOURCE"  )" && pwd)"

DAEMON="$DIR/bin/redis-server"
DAEMON_ARGS="$DIR/bin/redis.conf"
PIDFILE="$DIR/var/redis.pid"

set -e
case "$1" in
  start)
	start-stop-daemon --start --umask 007 --pidfile $PIDFILE \
        --chuid $SRVUSER --exec $DAEMON -- $DAEMON_ARGS
	;;
  stop)
	start-stop-daemon --stop --retry 10 --quiet --oknodo --pidfile $PIDFILE \
        --exec $DAEMON
	rm -f $PIDFILE
	;;

  restart|force-reload)
	${0} stop
	${0} start
	;;
  *)
	echo "Usage: $0 {start|stop|restart|force-reload}" >&2
	exit 1
	;;
esac

exit 0
