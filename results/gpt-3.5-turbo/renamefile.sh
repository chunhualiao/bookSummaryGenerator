
#This script does the following:

#Loops over all files in the current directory that match the pattern *-summary-txt.

#For each file, it constructs the new filename by replacing the trailing -summary-txt with .summary.txt. 
# This is done using parameter expansion: ${file%-summary-txt} removes the -summary-txt suffix from $file, and then .summary.txt is appended to form the new name.

#Renames the file using mv.


for file in *.summary.txt; do
    # Use parameter expansion to construct the new filename
    newname="${file%.txt}.md"
    # Rename the file
    mv "$file" "$newname"
done

