#!/bin/bash
python ./discord_send.py "$(date) - Starting monitoring service"

function cleanup()
{
  kill $PID_1 $PID_2 $PID_3
}


# Tracking
python track.py &
status=$?
PID_1=$!
if [ $status -ne 0 ]; then
  echo "Failed to start tracking: $status"
  exit $status
fi

# Alerting
python alert.py &
status=$?
PID_2=$!
if [ $status -ne 0 ]; then
  echo "Failed to start alerting: $status"
  exit $status
fi

# Dashboards
python dash_app.py &
status=$?
PID_3=$!
if [ $status -ne 0 ]; then
  echo "Failed to start dash application: $status"
  exit $status
fi

trap cleanup EXIT

# Naive check runs checks once a minute to see if either of the processes exited.
# This illustrates part of the heavy lifting you need to do if you want to run
# more than one service in a container. The container will exit with an error
# if it detects that either of the processes has exited.
# Otherwise it will loop forever, waking up every 60 seconds
  
while /bin/true; do
  ps aux |grep "python track.py" |grep -q -v grep
  PROCESS_1_STATUS=$?
  ps aux |grep "python alert.py" |grep -q -v grep
  PROCESS_2_STATUS=$?
  # If the greps above find anything, they will exit with 0 status
  # If they are not both 0, then something is wrong
  if [ $PROCESS_1_STATUS -ne 0 -o $PROCESS_2_STATUS -ne 0 ]; then
    echo "One of the processes has already exited."
    exit -1
  fi
  sleep 60
done
python ./discord_send.py "$(date) - Monitoring service ended, quitting, probably a crash!"
