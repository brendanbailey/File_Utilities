#File Splitter- Written by Brendan Bailey- 10/16/14
"""
The script takes a file and allows you to split into a number of files that the user designates. The files are relatively equal size.

The file must be a tab delimited text file.

An example use case is if you need to upload big data file that needs to be uploaded to a database, but the database has size limits of upload.
This script can be use to split the file into smaller pieces into order to load into the database.
"""
import csv, re, winsound
from Tkinter import *
from tkFileDialog import askopenfilename

def get_inputs():
	file_split = int(raw_input("Number of Files Need to Be Produced:\t"))
	Tk().withdraw()
	filename = askopenfilename() # show an "Open" dialog box and return the path to the selected file
	return filename, file_split
	
def process_file(filename, file_split):
	#Opens file to be split
	bulk_upload = open(filename, 'r')
	
	#Creates the files that are to be written to
	file_count = 0
	file_list = []
	while file_split > file_count:
		file = open(filename.replace('.txt','_part_'+str(file_count)+'.txt'),'w')
		file_list.append(file)
		file_count += 1

	#Writes header to new files
	first_line = bulk_upload.readline()
	for file in file_list:
		file.write(first_line)
	
	#Prints number of records in original file
	record_count = 0
	for line in bulk_upload:
		record_count += 1
	print record_count

	multiple = round(record_count/file_split)
	multiple_count = 0
	multiple_list = []
	while file_split > (multiple_count):
		multiple_multiplied = multiple * (multiple_count+1)
		print multiple_multiplied
		multiple_list.append(multiple_multiplied)
		multiple_count += 1

	if multiple_list[-1] != record_count:
		difference = multiple_list[-1] - record_count
		multiple_list[-1] = multiple_list[-1] - difference
		print multiple_list[-1]
	
	#Write to files
	bulk_upload = open(filename, 'r')
	first_line = bulk_upload.readline()
	line_count = 0
	write_count = 0
	while file_split > write_count:
		for line in bulk_upload:
			line_count += 1
			if line_count == record_count:
				file_list[write_count].write(line)
				write_count += 1
			elif line_count <= multiple_list[write_count]:
				file_list[write_count].write(line)
			else:
				file_list[write_count].write(line)
				write_count += 1

	bulk_upload.close()
	for file in file_list:
		file.close()
	print "File splitting complete"

filename, file_split = get_inputs()
process_file(filename, file_split)