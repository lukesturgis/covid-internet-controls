IFS=$'\n' read -d '' -r -a websites < website_list.txt ; echo ${websites[*]}

for i in "${websites[@]}"
do
echo $i
sudo python3 query_workers.py -t $i -v
sleep 5
done
