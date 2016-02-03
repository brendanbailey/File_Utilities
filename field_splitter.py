#Field Splitter- Written by Brendan Bailey- 5/18/15
"""
The script takes a file and allows you to split into multiple files based on the values within a field.

The file must be a tab delimited text file.

An example of a use case is that you a have big data file including data regarding various clients that needs to be split based, and sent to individual clients. 
If there is a client field, then you can split the file based on that column.
"""
import csv, re, winsound
from Tkinter import *
from tkFileDialog import askopenfilename

#Gets File Name
def load_file():
	print "Select the tab delimited text file you want to split"
	Tk().withdraw()
	filename = askopenfilename() # show an "Open" dialog box and return the path to the selected file
	return filename

#Asks user which field they would like to split on
def process_fields(filename):
	bulk_upload = open(filename, 'r')
	first_line = bulk_upload.readline()

	fields = first_line.split('\t')
	print "Ind","Field"
	for I, item in enumerate(fields):
		print I, item
	
	field_selected = int(raw_input("Select the index number of the field you would like to split the file on:"))

	values = []
	for line in bulk_upload:
		fields1 = line.split('\t')
		values.append(fields1[field_selected].strip())
	
	values = sorted(set(values))

	warning = False
	for item in values:
		print item
		if item.isalnum() is False:
			warning = True
	if warning == True:
		print "WARNING: There are non-alphanumeric characters in field values. This can cause errors."
	bulk_upload.close()
	print "\nNote: File Splitter strips out trailing White Space when sorting.\nFor example it will put California and Califorina*space* in the same file.\n"
	print "%s files will be created based on the above values" % len(values)
	proceed = raw_input("Enter Y to proceed\t")
	return proceed, values, field_selected

#Creates the files based on the field selected
def create_output(filename, proceed, values, field_selected):
	if proceed.upper() == "Y" or proceed.upper() == "YES":
		file_dictionary = {}
		bulk_upload = open(filename, 'r')
		first_line = bulk_upload.readline()
		for value in values:
			file_dictionary[value] = open(filename.replace('.txt','_%s.txt' % value), 'w')
			file_dictionary[value].write(first_line)
		for line in bulk_upload:
			fields1 = line.split('\t')
			file_dictionary[fields1[field_selected].strip()].write(line)
		for value in file_dictionary.values():
			value.close()
		bulk_upload.close()
		winsound.MessageBeep(48L)
		print "Field splitting complete"
	

filename = load_file()
proceed, values, field_selected = process_fields(filename)
create_output(filename, proceed, values, field_selected)