# 40 GB
SIZE="40"


# check the current size
CHECK="`du -sh /var/lib/docker/overlay2/ | cut -f1`"
echo "Current Foldersize: $CHECK GB"

# Get last character
last_char= "`echo "${CHECK:0-1}"`"

# Remove last character
CHECK="`echo ${CHECK:0:-1}`"

if  ["$last_char" = "M" ] || [ "$last_char" = "K" ];then
    break
elif (( $(echo "$CHECK > $SIZE" |bc -l) )); then
    docker system prune -a --volumes
else
    break
fi


