#!/usr/bin/python
#
# file 	 : genDoxygenC.py
# author : Srishti Parashar

import os
import sys
import re

########################################################################################################################################

RE_MULTI_LINE_PARAMS = ".*"

# could be used in header/source files, for method-definition extraction
RE_M_DEFINITION  = r'[A-Za-z0-9*]*\s*[A-Za-z0-9_*]+\s*[A-Za-z0-9_~:*]+\(.*\)\s*\{\s*.*?\s*\}'	#TODO:  this needs to be more generic to 														be able to parse for methods only
# used in header-files in major for method declaration extraction
RE_M_DECLERATION = r"[A-Za-z0-9*]*\s*[A-Za-z0-9_*]+\s+[A-Za-z0-9_~*]+\s*\(%s\)\s*;"%RE_MULTI_LINE_PARAMS
#RE_M_DECLERATION = r'[A-Za-z0-9*]*\s*[A-Za-z0-9_*]+\s*[A-Za-z0-9_~*]+\(.*\)\s*;'


########################################################################################################################################



# C/CPP CMD List
cmdList = ["for","if","while","switch","else"];

##########################
# exit errors enumerations
class EErrors() :
	IncorrectUsage, FileOpenError = range(2)

###################
# exception handler
def handleException(e, mssg) :
	if e == EErrors.IncorrectUsage :
		print "Usage : "+mssg
        elif e == EErrors.FileOpenError :
		print "Unable to open \"" + mssg + "\" file !"
	sys.exit(2)

###############################
# creates method doxygen header 
def frameDoxygenHeader(param_count, paramList) :
	commentStr = "/**\n * @brief \n" 	
	if param_count > 0 :
		for param in paramList:
			commentStr = commentStr + " * @param \n"
        
	# comment for return values
	commentStr = commentStr + " * @return \n */ \n"

	return commentStr

##############################################
# adds the doxygen comments, on method lookup
def addDoxygenComment(file_name, funcList) :
	try:	
		fh = open(file_name, 'rb')
		f_old = open(file_name, 'r+') 
	except:
                handleException(EErrors.FileOpenError, file_name)

	f_new = open(out_file_name, "w")
	final_loc = 0
	next_split_loc = 0
	last_write_loc = 0
	fContent = str(f_old.read())
	for func in funcList:
		SEARCH_TEXT = func	
		print "SEARCH_TEXT "+SEARCH_TEXT
	        fsize =  os.path.getsize(file_name)
	        bsize = fsize
	        word_len = len(SEARCH_TEXT)
		fh.seek(0)
		
		# doxygen comment header generation
		paramListStr = re.findall(r'\(.*\)', SEARCH_TEXT)
		paramListStr[0] = paramListStr[0].replace('(','')
		paramListStr[0] = paramListStr[0].replace(')','')
		paramList = paramListStr[0].split(",")
		comment_text = frameDoxygenHeader(len(paramList),paramList)
	        
		while True:
	               	found = 0
	               	pr = fh.read(bsize)
	               	pf = pr.find(SEARCH_TEXT, next_split_loc)
	               	if pf > -1:
	                       	found = 1
	                       	pos_dec = fh.tell() - (bsize - pf)
	                       	fh.seek(pos_dec + word_len)
	                       	bsize = fsize - fh.tell()
				print "Case-I:"+str(fh.tell())
	               	if fh.tell() < fsize:
	                               seek = fh.tell() - word_len + 1
	                               print "seek"+str(seek)
				       fh.seek(seek)
	                               if 1==found:
	                                       final_loc = seek
					       next_split_loc = final_loc + word_len - 1
	                                       print "loc: "+str(final_loc)
				       print "Case-IIa:"+str(fh.tell())
	               	else:
	                               break
				
		# create file with doxygen comments
		if final_loc != -1 :
			#f_new.write(fContent[0:final_loc-1]);
			#not to miss the contents, between two methods			
			if last_write_loc < final_loc :
				f_new.write(fContent[last_write_loc:final_loc-1]);
			
			f_new.write(comment_text);
			f_new.write(fContent[final_loc-1:next_split_loc])
			last_write_loc = next_split_loc
			
			#reset values
			final_loc = -1
		else:
			print "method not found !!"
		
	# last of the file should not be missed either
	if last_write_loc < len(fContent) :
		f_new.write(fContent[last_write_loc:]);
	f_new.close()
	f_old.close()


#############################################
#############################################
# main execution of the code starts from here
#############################################
argc = len(sys.argv)
if (argc == 1 or argc >2)  :
	handleException(EErrors.IncorrectUsage, "genDoxygenC.py <cpp source file>")
else :
	# Correct Input as per USAGE.
	fname = sys.argv[1]
	out_file_name = fname+'.doxygen'
	fcontent=''
	try:
		# read file
		fh = open(fname)
		fcontent = fh.read()
	#	print fcontent
	except:
		handleException(EErrors.FileOpenError, fname)
	
	# lookup for methods in file
	#prog = re.compile(RE_M_DECLERATION)
	#funcList = prog.match(fcontent)
        funcList = re.findall(RE_M_DECLERATION, fcontent, re.VERBOSE)
	fh.close()

	funcListCopy = funcList
	for fStr in funcListCopy :
		fStr = fStr.lstrip()
		startW = fStr.partition(' ')[0]
		startW = fStr.partition('(')[0]		#TODO: logic needs to be modified, with more cmds
		#print startW
		if startW in cmdList :
			# invalid method extraction			
			#print""
			funcList.remove(fStr)
		else :
			#print "Valid Method Extracted ::::  " + fStr
			print ""	

	# process valid methods-list for doxygen header
	addDoxygenComment(fname, funcList)
	#print funcList
