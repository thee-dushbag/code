logfile="client.log"
exec 50<"$logfile"
while read line; do
	echo $line
done <"$logfile"
if [ "$line" != "stop" ]; then echo stop; fi 
exec <&50-
