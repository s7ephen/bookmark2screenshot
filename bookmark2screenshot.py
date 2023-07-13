#!/usr/bin/env python2
# This script expects as input:
# A flat file full of URLs, one unique URL per line. 
# This can be done by exporting Brave/Chrome bookmarks to a file.
# For example if our exported bookmarks file is called "bookmarks_7_9_23.html":
# 
# $ cat bookmarks_7_9_23.html | sed -e 's/^A HREF="//' | awk -F\" '{ print $2 }' | sort | uniq > bookmarks_7_9_23.urls
#
# The resulting bookmarks_7_9_23.urls is sufficient as input for this tool.
# 
import sys
import os # for mkdir only
import re
import distutils.spawn #for find_executable to make sure we have what we need.
import md5
import subprocess
import time # for unique file/dir names
import json # we write a logfile in json
import urllib # for urlencoding
import signal # maybe for forcibly terminating the subprocess.

def Usage():
  print "USAGE: "
  print sys.argv[0]," <filename of bookmark file>"
  thing = '''
INPUT: 

\tThis tool expects as input a flat file full of URLs, one unique URL per line.
\tThis can be done by exporting Brave/Chrome bookmarks to a file.
\t For example if our exported bookmarks file is called "bookmarks_7_9_23.html":

$ cat bookmarks_7_9_23.html | sed -e 's/^A HREF="//' | awk -F\" '{ print $2 }' | sort | uniq > bookmarks_7_9_23.urls

\tThe resulting bookmarks_7_9_23.urls is sufficient as input for this tool.

'''
  print thing

if len(sys.argv) <= 1:
    Usage()
    sys.exit(0)

print "Opening this file for URLs: %s" % sys.argv[1]
f_h = open(sys.argv[1], mode='r')
f_contents = f_h.readlines()
f_h.close()

print "Found %d URLs in file." % len(f_contents)
if len(f_contents) > 6:
    print "Previewing first 5 urls: " 
    for line in f_contents[:5]:
        print "\t",line,  #no newline because each line already has one from the file
    print "Previewing last 5 urls: " 
    for line in f_contents[len(f_contents)-5:len(f_contents)]:
        print "\t",line,  #no newline because each line already has one from the file
else:
    print "Previewing contents of file:"
    for line in f_contents:
        print "\t",line,  #no newline because each line already has one from the file

print ("\n\nSearching for firefox executable...")
ff_path = distutils.spawn.find_executable("firefox")
if ff_path == None:
   print "\t!!! Firefox not installed or in $PATH. You need it for this tool. Exiting."
   sys.exit(1)
else:
  print "\tFound Firefox at: %s" % ff_path

# *********************
# ** Screenshotting ***
# *********************
print "\n\n COMMENCING SCREENSHOTS!"
print "NOTE: YOU CAN NOT HAVE FIREFOX ALREADY RUNNING!!!"
print "   since some output from firefox is muted here (to keep the screen neat)"
print "   you would not see the warning from firefox about this."
#screensdir = "./marks2screens_%d" % int(time.time())
screensdir = "./marks2screens" # I was using unique directories but gave up on this
                               # because sometimes in large image dirs, you interrupt and want
                               # to continue later.
if os.path.exists(screensdir):
    print "\nUsing Existing Screenshots directory: %s'" % screensdir
else:
    print "\nCreating Screenshots directory: '%s'" % screensdir
    os.mkdir(screensdir)
i = 0
logdict = dict()
for line in f_contents:
    i+=1
    url = line.replace("\n","")
    url_digest=md5.md5(url).hexdigest()
    url_png = url_digest+".png"
    url_txt = url_digest+".txt"
    urltxt_name = screensdir+'/'+url_txt
    print "Screenshot # %d: (%s)" % (i, time.asctime())
    print "\t URL: %s" % url
    print "\t Screenshot file: %s.png" % url_digest
    print "\t Screenshot URL file: %s" %  url_txt
    command = "firefox -headless -private-window -screenshot %s/%s %s " % (screensdir,url_png,url)
    logdict[url_png] = url
    if os.path.isfile(screensdir+"/"+url_png):
        print "\t\t THIS SCREENSHOT ALREADY EXISTS, SKIPPING!"
        continue
    print "\t Executing `%s`. " % command
    #process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
    process = subprocess.Popen(command, shell=True, stdout=None, stderr=subprocess.PIPE) # dont receive output from the program unless it is an error
    process.wait()
    #print "\t",process.returncode
    url_txt_h = open(urltxt_name, 'w')
    # url = urllib.quote_plus(url) # raw URLs might break FGallery HTML syntax, so this might help.
    url_txt_h.write(url+"\n"+url) # For this FGallery text file feature, first line is Title, second is Description
    url_txt_h.close()
#    print repr(logdict),len(logdict.keys())
print "\n****** SCREENSHOTS COMPLETE ******"
logdict_fname = "bookmark2screenshot_log.json"
l_name = screensdir+'/'+logdict_fname
print "Dumping Bookmark to Screenshot log to file: %s" % l_name
log_h = open(l_name, 'a') # Append mode just in case it already existed from previous run
json.dump(logdict, log_h)
log_h.close()
