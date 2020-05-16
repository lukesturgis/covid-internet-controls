python3 test.py | grep AS[0-9] > t.txt ; sed -i 's/Data  : AS//g' t.txt ; sed '1,100!d' t.txt > t_final.txt ; IFS=$'\n' read -d '' -r -a lines < t_final.txt ; echo ${lines[*]}
