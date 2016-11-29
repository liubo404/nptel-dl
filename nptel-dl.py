#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This Python script generates text file containing all the URLs of a corresponding NPTEL course.

from robobrowser import RoboBrowser
import json 
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("url", help ="Input the URL of the course in nptel.ac.in/courses/ format", type =str)
parser.add_argument("quality",help ="Input the video quality you want. 0 for low quality, 1 for medium, 2 for high quality")

args = parser.parse_args()

try:
    browser = RoboBrowser(parser='html.parser', user_agent='Mozilla')
    browser.open(args.url)
    script = browser.find_all("script", type="application/ld+json")

    info = ""
    for element in script[0]:
        info = info + element
    infodict = json.loads(info)

    # time for some fancy outputs 

    print 'Course Detected: {} '.format(infodict["name"])
    print 'Number of Videos to download:  {} '.format(len(infodict['partOfEducationalTrack']))

    vidurllist = []
    quality = 2-int(args.quality)
    for vidurl in infodict['partOfEducationalTrack']:
        #print vidurl
        print ' Getting URL of Video Number: {} '.format(len(vidurllist)+1)
        browser.open(vidurl)
        hyplink = browser.find_all("a", text = "Mirror 1")
        vidurllist.append(hyplink[quality].get("href"))

    filename = infodict['name'].replace(' ','_') + '.txt'
    thefile = open(filename, 'w')
    for item in vidurllist:
      print>>thefile, item
except Exception as e:
    print e

