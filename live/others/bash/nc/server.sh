logfile="server.log"
exec 51>"$logfile"
for current in {1..50}; do
	echo -n "Enter line $current: "
	read data
	if [ -z "$data" ]; then continue; fi
	if [ "$data" == "stop" ]; then break; fi
	echo >&51 "Received: $data"
done
exec >&52-
