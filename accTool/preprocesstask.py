from celery import task

import subprocess
import os
from os import listdir
import re
username = "pdf"
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
USER_FOLDER = BASE_DIR +  "/media/upload/" + username + "/"
USER_PP_FOLDER = USER_FOLDER + "pp/"
PARSE_PY = BASE_DIR + "/accTool/static/py/pdfminer/tools/pdf2txt.py"

@task()
def preprocess(inputfile):
	# Create empty file
	open(USER_PP_FOLDER+ 'alttext.txt', 'a').close()
	ag1 = BASE_DIR + "/accTool/static/jar/javatool.jar"
	ag2 = USER_FOLDER + inputfile
	ag3 = USER_PP_FOLDER + 'Img%s.%s'
	ag4 = USER_PP_FOLDER+ 'alttext.txt'
	print ag1
	print ag2
	print ag3
	print ag4
	subprocess.call(['java', '-jar', ag1, '-p', ag2,ag3,ag4])
	
	# parse text
	os.system("python " + PARSE_PY + " -o " + USER_PP_FOLDER+"ogtext.txt " + ag2)