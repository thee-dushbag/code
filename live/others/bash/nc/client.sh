logfile="client.log"
exec 50<"$logfile"
while read line; do
	echo $line
done <&50
if [ "$line" != "stop" ]; then echo stop; fi 
exec <&50-
