#!/usr/bin/env python
import datetime
import time
import os
from urllib import pathname2url 
from xml.sax.saxutils import escape

BASE_DIR = '/media'
BASE_URL = '${BASE_URL}'
INDEX_FILENAME = 'index.xml'

MIME_TYPES = {
              'aac':'audio/mpeg',
              'avi':'video/avi',
              'mp4':'video/mpeg',
              'sub':'image/vnd.dvb.subtitle',
              'mkv':'video/x-matroska',
              'nfo':'text/plain',
              'srt':'text/plain'
              }

# import constants from stat library
from stat import * # ST_SIZE ST_MTIME

# format date method
def formatDate(dt):
    return dt.strftime("%a, %d %b %Y %H:%M:%S +0000")

# get the item/@type based on file extension
def getItemType(fileExtension):
    return MIME_TYPES.get(fileExtension)

def generateRSS(outputFile, baseDirectory, baseURL):
  # constants
  # the podcast name
  rssTitle = "Files"
  # the podcast description
  rssDescription = "sabnzbd files"
  # the url where the podcast items will be hosted
  rssSiteURL = 'http://invalid/'
  # the url of the folder where the items will be stored
  rssItemURL = baseURL
  # the url to the output html file
  rssLink = outputFilename
  # the time to live (in minutes)
  rssTtl = "60"
  # contact details of the web master
  rssWebMaster = "me@me.com"

  #record datetime started
  now = datetime.datetime.now()
  
  # write rss header
  outputFile.write("<?xml version=\"1.0\" encoding=\"UTF-8\" ?>\n")
  outputFile.write("<rss version=\"2.0\">\n")
  outputFile.write("<channel>\n")
  outputFile.write("<title>" + rssTitle + "</title>\n")
  outputFile.write("<description>" + rssDescription + "</description>\n")
  outputFile.write("<link>" + rssLink + "</link>\n")
  outputFile.write("<ttl>" + rssTtl + "</ttl>\n")
  outputFile.write("<copyright>mart 2012</copyright>\n")
  outputFile.write("<lastBuildDate>" + formatDate(now) + "</lastBuildDate>\n")
  outputFile.write("<pubDate>" + formatDate(now) + "</pubDate>\n")
  outputFile.write("<webMaster>" + rssWebMaster + "</webMaster>\n")


  # walk through all files and subfolders 
  for path, subFolders, files in os.walk(baseDirectory):
      for file in files:
          # split the file based on "." we use the first part as the title and the extension to work out the media type
          if file.find('_UNPACK_') > -1:
  	    continue
          if file.lower().find('sample.') > -1:
              continue
          fileNameBits = file.split(".")
          extension = fileNameBits[len(fileNameBits)-1].lower()
          itemType = getItemType(extension)
          if not itemType:
              continue
          # get the full path of the file
          fullPath = os.path.join(path, file)
          # get the stats for the file
          fileStat = os.stat(fullPath)
          # find the path relative to the starting folder, e.g. /subFolder/file
          relativePath = fullPath[len(baseDirectory):]

          title = ''
          if extension == 'nfo':
              title = ' info'
          elif extension in ('sub', 'srt'):
              title = ' subtitles'

          if relativePath.startswith('/'):
            relativePath = relativePath[1:]

          rawlink = os.path.join(rssItemURL, relativePath)
          link = os.path.join(rssItemURL, pathname2url(relativePath))
          # write rss item
          outputFile.write("<item>\n")
          outputFile.write("<title>" + escape('.'.join(fileNameBits[:-1]).replace("_", " ") + title) + "</title>\n")
          outputFile.write("<description>A description</description>\n")
          outputFile.write("<link>" + escape(link) + "</link>\n")
          outputFile.write("<guid>" + escape(rawlink) + "</guid>\n")
          outputFile.write("<pubDate>" + formatDate(datetime.datetime.fromtimestamp(fileStat[ST_MTIME])) + "</pubDate>\n")
          outputFile.write("<enclosure url=\"" + escape(link) + "\" length=\"" + str(fileStat[ST_SIZE]) + "\" type=\"" + itemType + "\" />\n")
          outputFile.write("</item>\n")

  # write rss footer
  outputFile.write("</channel>\n")
  outputFile.write("</rss>")

if __name__ == '__main__':
  outputFilename = os.path.join(BASE_DIR, INDEX_FILENAME)
  with open(outputFilename, "w") as outputFile:
    generateRSS(outputFile, BASE_DIR, BASE_URL)
  print "Completed %s" % outputFilename
