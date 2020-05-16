import json # pretty print nested hash
L = ["Geeks\n", "for\n", "Geeks\n"] 
#	 print("{}:{}:{}".format(as_array[0],as_array[1],as_array[2]))	
#        print("Line{}: {}".format(count, line.strip())) # Writing to file   
# Using for loop 
count = 0
as_array = []
as_relationship_list = []
as_chidrens= [[0 for i in range(10000)] for j in range(10000)]

with open("20200501_as_rel.txt") as fp: 
    for line in fp: 
        count += 1
	as_array = line.split('|')
	if as_array[2] == "-1\n": 
#		as_array[0], as_array[1] = as_array[1], as_array[0]	
		as_chidrens[int(as_array[0])][int(as_array[1])] = "YES"
		as_relationship_list.append(as_array[0:2])

print(as_relationship_list[-1])
print(as_chidrens)

with open("mytestfile.txt", "w") as fp: 
    fp.writelines(L) 
