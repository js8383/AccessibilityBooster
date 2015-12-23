from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib.auth.decorators import login_required  
from django import forms
from django.shortcuts import render,render_to_response
from django.template import RequestContext
from django.contrib.auth import authenticate, login, logout
from accTool.models import Document,ParsedImage,Headings,Metadata
from accTool.forms import DocumentForm
from django.core.urlresolvers import reverse
import subprocess
import os
from os import listdir
import re
import shutil
# from util import preprocess
import threading
from django.contrib import messages
from django.http import HttpResponse
# from django.core.servers.basehttp import FileWrapper
# from django.core.files.base import ContentFile
# from django.utils.six import b

from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument

# For preprocessing
username = "pdf"
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
USER_FOLDER = BASE_DIR +  "/media/upload/" + username + "/"
USER_PP_FOLDER = USER_FOLDER + "pp/"
USER_OP_FOLDER = USER_FOLDER + "output/"
PARSE_PY = BASE_DIR + "/accTool/static/py/pdfminer/tools/pdf2txt.py"
USER_FOLDER_DJANGO = "/media/upload/" + username + "/"

# Create your views here.

@login_required
def preview_pdf(request):
    filename = ""
    for f in listdir(USER_FOLDER):
        if f.endswith(".pdf"):
            filename = f
	return render(request, 'd_preview.html', {'pdflink': USER_FOLDER_DJANGO + filename})

@login_required
def upload_pdf(request):
    return render(request, 'd_upload.html')


def user_login(request):
    # Like before, obtain the context for the user's request.
    context = RequestContext(request)

    # If the request is a HTTP POST, try to pull out the relevant information.
    if request.method == 'POST':
        # Gather the username and password provided by the user.
        # This information is obtained from the login form.
        username = request.POST['username']
        password = request.POST['password']

        # Use Django's machinery to attempt to see if the username/password
        # combination is valid - a User object is returned if it is.
        user = authenticate(username=username, password=password)

        # If we have a User object, the details are correct.
        # If None (Python's way of representing the absence of a value), no user
        # with matching credentials was found.
        if user:
            # Is the account active? It could have been disabled.
            if user.is_active:
                # If the account is valid and active, we can log the user in.
                # We'll send the user back to the homepage.
                login(request, user)
                return HttpResponseRedirect('/upload/')
            else:
                # An inactive account was used - no logging in!
                return HttpResponse("Your Rango account is disabled.")
        else:
            # Bad login details were provided. So we can't log the user in.
            print "Invalid login details: {0}, {1}".format(username, password)
            return HttpResponse("Invalid login details supplied.")

    # The request is not a HTTP POST, so display the login form.
    # This scenario would most likely be a HTTP GET.
    else:
        # No context variables to pass to the template system, hence the
        # blank dictionary object...
        return render_to_response('login.html', {}, context)

@login_required
def user_logout(request):
    # Since we know the user is logged in, we can now just log them out.
    logout(request)

    # Take the user back to the homepage.
    return HttpResponseRedirect('/login/')

@login_required
def upload_pdf(request):
    # Handle file upload
    fileT = "empty"
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            newdoc = Document(docfile=request.FILES['docfile'])
            if newdoc.extension() == ".pdf":
                fileT = "pdf"
                shutil.rmtree(USER_FOLDER)
                os.makedirs(USER_FOLDER)
                os.makedirs(USER_PP_FOLDER)
                os.makedirs(USER_OP_FOLDER)
                newdoc.save()
                filename = ""
                for f in listdir(USER_FOLDER):
                    if f.endswith(".pdf"):
                        filename = f
                preprocess(filename)
                # messages.info(request, 'Complete')
                return HttpResponseRedirect('/home/')
            else:
                fileT = "other"
        else:
            fileT = "empty1"

            # Redirect to the document list after POST
            # return HttpResponseRedirect(reverse('accTool.views.upload_pdf'))
    else:
        form = DocumentForm()  # A empty, unbound form


    # Render list page with the documents and the form
    return render_to_response(
        'd_upload.html',
        {'form': form, 'fileT': fileT},
        context_instance=RequestContext(request)
    )

@login_required
def image_preview(request):
    return render(request, 'd_imagep.html',{'Images': ParsedImage.objects.all()})

def upload_progress(request):
    # preprocess("input11.pdf")
    return render(request, 'd_imagep.html',{'Images': ParsedImage.objects.all()})


def preprocess(inputfile):
    ParsedImage.objects.all().delete()
    Headings.objects.all().delete()
    # Create empty file
    open(USER_PP_FOLDER+ 'alttext.txt', 'a').close()
    ag1 = BASE_DIR + "/accTool/static/jar/javatool.jar"
    ag2 = USER_FOLDER + inputfile
    ag3 = USER_PP_FOLDER + 'Img%s.%s'
    ag4 = USER_PP_FOLDER+ 'alttext.txt'
    # print ag1
    # print ag2
    # print ag3
    # print ag4
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
        imgName = numl[i][1]
        altText = lines[i].rstrip('\x00').rstrip('\n')
        # if altText == "None":
        # tmp = ParsedImage(order=i, cacheLink=USER_FOLDER_DJANGO + "pp/" + imgName)
        # else:
        tmp = ParsedImage(order=i, cacheLink=USER_FOLDER_DJANGO + "pp/" + imgName, altText = altText)
        tmp.save()

    parse()
    metadata()

def applytag():
    inputfile = ""
    for f in listdir(USER_FOLDER):
        if f.endswith(".pdf"):
            inputfile = f
    ag1 = BASE_DIR + "/accTool/static/jar/javatool.jar"
    ag2 = USER_FOLDER + inputfile
    ag3 = USER_OP_FOLDER + "modified_" + inputfile
    ag4 = USER_PP_FOLDER+ 'newAlttext.txt'
    print ag1
    print ag2
    print ag3
    print ag3
    print inputfile
    subprocess.call(['java', '-jar', ag1, '-o', ag2,ag3,ag4])

def image_alt(request):
    return render(request, 'd_imagealt.html',{'Images': ParsedImage.objects.all()})

@login_required
def image_alt_submit(request):
    context = RequestContext(request)
    filename = USER_PP_FOLDER + "newAlttext.txt"
    if os.path.exists(filename):
        os.remove(filename)
    f = open(filename, 'w')
    if request.method == 'POST':
        i = 0
        while True:
            if str(i) not in request.POST:
                break
            newAlttext = request.POST[str(i)]
            if newAlttext != "":
                ParsedImage.objects.filter(order=i).update(altText=newAlttext)
            i += 1
       
        j = 0
        while True:
            try:
                x = ParsedImage.objects.get(order=j)
                f.write(x.altText+"\n")
            except ParsedImage.DoesNotExist:
                break
            j += 1
        f.close()
        applytag()
        return render(request, 'd_imagealt.html',{'Images': ParsedImage.objects.all()})
    else:
        return render(request, 'd_imagealt.html',{'Images': ParsedImage.objects.all()})

@login_required
def image_alt_export(request):
    inputfile = ""
    for f in listdir(USER_FOLDER):
        if f.endswith(".pdf"):
            inputfile = f
    ag1 = USER_OP_FOLDER + "modified_" + inputfile
    ag2 = "s3://jason15319/pdfpdfpdfpdf/" + "modified_" + inputfile
    # print ag1, ag2
    subprocess.call(['s3cmd', 'put', "-P", ag1, ag2])
    return HttpResponseRedirect("http://jason15319.s3.amazonaws.com/pdfpdfpdfpdf/" + "modified_" + inputfile)

@login_required
def heading_preview(request):
    return render(request, 'd_headings.html',{'Headings': Headings.objects.all()})

def metadata_preview():
    return render(request, 'd_headings.html',{'Metadata': Metadata.objects.all()})

###################################################

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
    i = 0
    for heading in result_headings:
        if heading != "":
            tmp = Headings(heading = heading, order = i)
            tmp.save()
            i += 1

def metadata():
    # inputfile = ""
    # for f in listdir(USER_FOLDER):
    #     if f.endswith(".pdf"):
    #         inputfile = f
    # fp = open(USER_FOLDER + inputfile, 'rb')
    # parser = PDFParser(fp)
    # doc = PDFDocument(parser)
    # dic = doc.info[0]  # The "Info" metadata
    # i = 0
    # for k, v in dic.iteritems():
    #     tmp = Metadata(k = str(k), v = str(v), order = i)
    #     tmp.save()
    #     i += 1
    return
