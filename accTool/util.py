import subprocess
import os
from os import listdir
import re
from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument
# from accTool.models import ParsedImage

username = "pdf"
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
USER_FOLDER = BASE_DIR +  "/media/upload/" + username + "/"
USER_PP_FOLDER = USER_FOLDER + "pp/"
PARSE_PY = BASE_DIR + "/accTool/static/py/pdfminer/tools/pdf2txt.py"
USER_FOLDER_DJANGO = "/media/upload/" + username + "/"
USER_OP_FOLDER = USER_FOLDER + "output/"

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

	# Add to table
	numl = []
	for f in listdir(USER_PP_FOLDER):
		if not f.endswith((".jpg", ".png")):
			continue
		ff = f[3::]
		od = ff.split(".")[0]
		numl += [(int(od), f)] 
	numl.sort(key=lambda tup: tup[0])
	print numl

	with open(USER_PP_FOLDER+ 'alttext.txt') as f: lines = f.readlines()
	size = min(len(numl),len(lines))
	for i in xrange(size):
		print numl[i][1], lines[i].rstrip('\x00').rstrip('\n')
		# tp = numl[i]
		# if tp[1] == "None":
		# 	tmp = ParsedImage(cacheLink=USER_FOLDER_DJANGO + "pp/" + tp[0], altText= t)
		# else:
		# 	tmp = ParsedImage(cacheLink=USER_FOLDER_DJANGO + "pp/" + tp[0], altText= tp[1])
		# tmp.save()

# print PARSE_PY
# preprocess("input11.pdf")
for f in listdir(USER_FOLDER):
	if f.endswith(".pdf"):
		filename = f
		print USER_FOLDER + filename

def image_alt_export():
    inputfile = ""
    for f in listdir(USER_FOLDER):
        if f.endswith(".pdf"):
            inputfile = f
    ag1 = USER_OP_FOLDER + "modified_" + inputfile
    ag2 = "s3://jason15319/pdfpdfpdfpdf/" + "modified_" + inputfile
    print ag1, ag2

# image_alt_export()

def getmeta():
    fp = open(USER_FOLDER + "input1.pdf", 'rb')
    parser = PDFParser(fp)
    doc = PDFDocument(parser)
    dic = doc.info[0]  # The "Info" metadata
    for key, value in dic.iteritems():
    	print key, value
    

getmeta()

