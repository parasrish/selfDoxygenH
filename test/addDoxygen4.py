#!/usr/bin/python

import os
import sys

# exit errors enumerations
class EErrors() :
        IncorrectUsage, FileOpenError = range(2)

# exception handler
def handleException(e, mssg) :
        if e == EErrors.IncorrectUsage :
                print "Usage : addDoxygen4.py <cpp source file> <method text>"
        elif e == EErrors.FileOpenError :
                print "Unable to open \"" + mssg + "\" file !"
        sys.exit(2)


SEARCH_TEXT = ""
file_name = ''
out_file_name = ''
comment_text = '\n/**\n *\n *\n */\n'

final_loc = -1
# main execution of the code starts from here
argc = len(sys.argv)
print argc
if argc < 3 :
        handleException(EErrors.IncorrectUsage, "")
else :
        # Correct Input as per USAGE.
        file_name = sys.argv[1]
	out_file_name = file_name+'.doxygen'
        # create search-method-text-here
	for word in sys.argv[2:argc]:
		SEARCH_TEXT = SEARCH_TEXT+" "+word
        print "SEARCH_TEXT :"+SEARCH_TEXT
	fh=''
	try:
                # lookup of the method-text here
                fh = open(file_name, 'rb')
	except:
                handleException(EErrors.FileOpenError, file_name)

        fsize =  os.path.getsize(file_name)
        bsize = fsize
        word_len = len(SEARCH_TEXT)
        while True:
               	found = 0
               	pr = fh.read(bsize)
               	pf = pr.find(SEARCH_TEXT)
               	if pf > -1:
                       	found = 1
                       	pos_dec = fh.tell() - (bsize - pf)
                       	fh.seek(pos_dec + word_len)
                       	bsize = fsize - fh.tell()
               	if fh.tell() < fsize:
                               seek = fh.tell() - word_len + 1
                               fh.seek(seek)
                               if 1==found:
                                       final_loc = seek
                                       print "loc: "+str(final_loc)
               	else:
                               break

# create file with doxygen comments
if final_loc != -1 :
	f_old = open(file_name,'r+') 
	f_new = open(out_file_name, "w")
	f_old.seek(0)
	fStr = str(f_old.read())
	f_new.write(fStr[:final_loc-1]);
	f_new.write(comment_text);
	f_new.write(fStr[final_loc-1:])
	f_new.close()
	f_old.close()
else:
	print "method not found !!"
