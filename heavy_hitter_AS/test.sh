#python3 test.py | grep AS[0-9] > t.txt ; sed -i 's/Data  : AS//g' t.txt ; sed '1,100!d' t.txt > t_final.txt ; IFS=$'\n' read -d '' -r -a lines < t_final.txt ; echo ${lines[*]}


IFS=$'\n' read -d '' -r -a countries < countries_list.txt ; echo ${countries[*]}
A="full_AS_list.txt"
B="top_AS_list.txt"
for i in "${countries[@]}"
do
echo $i
C=$i$A
D=$i$B
C="${C/countries/}" 
C="${C/.html/_}" 
C="${C/'/'/}" 
D="${D/countries/}" 
D="${D/.html/_}" 
D="${D/'/'/}" 
#echo $C
#echo $D
#python3 heavy_hitter_list_of_all_AS_in_country_list.py $i
python3 heavy_hitter_list_of_all_AS_in_country_list.py $i| grep AS[0-9]|grep -v -e '"' > $C ; sed -i 's/Data  : AS//g' $C ; sed '1,100!d' $C > $D; IFS=$'\n' read -d '' -r -a lines < $D ; echo ${lines[*]}
#pkill python3
done
