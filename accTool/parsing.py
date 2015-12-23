import subprocess
import os
from os import listdir
import re
import shutil

username = "pdf"
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
USER_FOLDER = BASE_DIR +  "/media/upload/" + username + "/"
USER_PP_FOLDER = USER_FOLDER + "pp/"
USER_OP_FOLDER = USER_FOLDER + "output/"
PARSE_PY = BASE_DIR + "/accTool/static/py/pdfminer/tools/pdf2txt.py"
USER_FOLDER_DJANGO = "/media/upload/" + username + "/"

KEY_START_WORD = ["ABSTRACT"]
KEY_END_WORD = ["REFERENCES"]


def parse():
	f = open(USER_PP_FOLDER + "ogtext.txt")
	lines = f.readlines()
	result_headings = []
	# result_paragraphs = []
	begin = False
	llines = []
	for line in lines:
		l = line.rstrip("\n").strip()
		llines += [l]
	lens = len(llines)

	current_heading = ""
	# current_p = ""
	# print llines

	for i in xrange(lens):
		line = llines[i]
		if line in KEY_START_WORD:
			begin = True
		if line in KEY_END_WORD:
			break
		if not begin:
			continue

		if line == "": 
			continue

		#
		if line.isupper(): # and llines[i-1]=="\n":
			if len(line) > 50:
				continue
			if not line.replace(" ", "").isalnum():
				continue
			result_headings += [current_heading]
			# result_paragraphs += current_p
			current_heading = line
			# current_p = ""
			continue
	    #
		if line[0].isupper():
			if llines[i+1] != "" and llines[i+1][0].isupper():
				if len(line) > 40:
					continue
				if len(llines[i+1]) < 20:
					continue
				if not line.replace(" ", "").isalnum():
					continue
				result_headings += [current_heading]
				current_heading = line
				continue
			if llines[i+1] != "" and llines[i+1][0].islower() and llines[i-1] == "" :
				continue

		# current_p += line
		
		# if i > 800: break


	print result_headings


parse()