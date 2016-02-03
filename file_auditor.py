#File Auditor - Written by Brendan Bailey and refactored by George Jansen - 5/5/14
"""This script audits all files in a directory. 
The audit produces a tab delimited report showing the cover and count for all fields and a 20 record sample in each file."""

import os, datetime, random

#Asks user for directory they would like to process
def ask_directory():
	
	print """The following script is used to audit files in a given directory. 
	i.e. C:\Users\etc...

	Enter in the folder directory where all these files are located.
	There should be no other folders within directory.

	If there are spaces within the directory name, please use double quotes to 
	frame the directory "C:\Users\et cetera..."
	
	The resulting text document will indicate how many records 
	and fields are in each file.

	The script will also randomly sample 20 records from each file"""
	print "\n"
	indir = raw_input("Enter Folder Directory-->").replace('"','')
	return indir

#Processes the individual file
def process_file(ofh, input_path):
    ifh = open(input_path, 'r')
    print "Starting %s" % input_path
    header = ifh.readline()
    names = header.split("\t")
    nfields = len(names)
    counts = [0 for i in range(0,nfields)]
    samples = ['' for i in range(0,20)]
    data_recs = 0
    random.seed()
    for line in ifh:
        fields = line.rstrip().split("\t")
        for i in range(0, len(fields)):
            if fields[i] != '':
                counts[i] += 1
        rand = random.randint(0,data_recs)
        if rand < 20:
            samples[rand % 20] = line
        data_recs += 1
        if data_recs % 100000 == 0:
            print "At record %d" % data_recs

    ifh.close()
    percentages = ["%d%%" % (((x * 100))/data_recs) for x in counts]
    
    ofh.write("Number of fields:\t%d\n" % nfields)
    ofh.write("Total Records:\t%d\n" % data_recs)
    ofh.write("Coverage\n")
    ofh.write("%s\n" % "\t".join(['%d' % x for x in counts]))
    ofh.write("%s\n" % "\t".join(percentages))
    ofh.write(header)
    for line in samples:
        ofh.write(line)
    ofh.write("\n")	

#Processes all files in a directory
def process_directory(indir):
	i = datetime.datetime.now()
	audit_name = "file_audit_" + str(i.month) + "_" + str(i.day) + "_" + str(i.year) + "_" + str(i.hour) + "_" + str(i.minute) + ".txt"
	ofh = open(audit_name,'w')
	for root, dirs, filenames in os.walk(indir):
		for f in filenames:
			input_path = os.path.join(root, f)
			print "Starting: " + f
			ofh.write("File:\t" + f + "\n") #Writes file name to output
			#process_file(ofh, input_path)
			try:
				process_file(ofh, input_path)
			except:
				print "File Error\n"
				ofh.write("File Error\n\n")
	ofh.close()

indir = ask_directory()
process_directory(indir)