# Essential files and folders required to run heavy hitter AS program
1. countries/
2. 20200501_as_rel.txt
3. asrelationship.py
4. countries_list.txt
5. heavy_hitter_list_of_all_AS_in_country_list.py
6. heavy_hitter_list_of_all_AS_in_country_list.sh

# Run the process
1. $./heavy_hitter_list_of_all_AS_in_country_list.sh

Note: All the pattern (for AS number parsing) to include and exclude need to be added in shell script.

# Output files:
1. File having top in file name contain top 20 ASes
2. File having full in file name conatin all ASes
3. File having heavy hitter and country in file name contain final heavy hitter ASes list 
4. as_relationship_graph.txt contain parent-child cone graph from caida ASes relationship dataset

# ToDo
1. Optimize % of internet cover code. Currently commented in asrelationship.py file.
