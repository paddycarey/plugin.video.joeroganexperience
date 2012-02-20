#!/usr/bin/env python

import os
import re
import sys
import urllib
import urllib2

import xbmc
import xbmcaddon
import xbmcgui
import xbmcplugin

import StorageServer

from resources.lib import vimeo
from resources.lib import ustream

### get addon info
__addon__             = xbmcaddon.Addon()
__addonid__           = __addon__.getAddonInfo('id')
__addonidint__        = int(sys.argv[1])
__addondir__          = xbmc.translatePath(__addon__.getAddonInfo('path'))

# initialise cache object to speed up plugin operation
cache = StorageServer.StorageServer(__addonid__ + '-videos', 24)

def getParams():
    
    """Parse and return the arguments passed to the addon in a usable form
    
    Returns:    param -- A dictionary containing the parameters which have been passed to the addon"""
    
    # initialise empty list to store params
    param=[]
    
    # store params as string
    paramstring=sys.argv[2]
    
    # check if params were provided
    if len(paramstring)>=2:
        
        # store params as string
        params=sys.argv[2]
        
        # remove ? from param string
        cleanedparams=params.replace('?','')
        
        # check if last argument is /
        if (params[len(params)-1]=='/'):
            params=params[0:len(params)-2]
        
        # split param string into individual params
        pairsofparams=cleanedparams.split('&')
        
        # initialise empty dict to store params
        param={}
        
        # loop through all params
        for i in range(len(pairsofparams)):
            
            # initialise empty dict to store split params
            splitparams={}
            
            # get name and value of param
            splitparams=pairsofparams[i].split('=')
            
            # check if param has value
            if (len(splitparams))==2:
                
                # add value to param dict
                param[splitparams[0]]=splitparams[1]
    
    # return dict of params
    return param

def getHtml(url):
    
    """Retrieve and return remote resource as string
    
    Arguments:  url -- A string containing the url of a remote page to retrieve
    Returns:    data -- A string containing the contents to the remote page"""

    # Build the page request including setting the User Agent
    req  = urllib2.Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')

    # connect to url using urlopen
    client = urllib2.urlopen(req)
    
    # read data from page
    data = client.read()
    
    # close connection to url
    client.close()
    
    # return the retrieved data
    return data

def log(txt, severity=xbmc.LOGDEBUG):
    
    """Log txt to xbmc.log at specified severity
    
    Arguments:  txt -- A string containing the text to be logged
                severity -- Logging level to log text at (Default to LOGDEBUG)"""

    # generate log message from addon name and txt
    message = ('%s: %s' % (__addonid__, txt))
    
    # write message to xbmc.log
    xbmc.log(msg=message, level=severity)

def addVideo(linkName = '', url = '', thumbPath = '', date = ''):
    
    """Add a video to an XBMC directory listing
    
    Arguments:  linkName -- A string containg the name of the video
                url -- A string containing the direct url to the video
                thumbPath -- A string containg the url/path of the video's thumbnail image
                date -- a dataetime object containg the date of the video"""
    
    finalUrl = sys.argv[0] + "?url=" + urllib.quote_plus(url)
    
    # initialise a listitem object to store video details
    li = xbmcgui.ListItem(linkName, iconImage = thumbPath, thumbnailImage = thumbPath)
    
    # set the video to playable
    li.setProperty("IsPlayable", 'true')
    
    # set the infolabels for the video
    li.setInfo( type="Video", infoLabels={ "title": linkName, "date":date} )
    
    # set fanart image for video
    li.setProperty( "Fanart_Image", os.path.join(__addondir__, 'fanart.jpg'))
    
    # add listitem object to list
    xbmcplugin.addDirectoryItem(handle = __addonidint__, url = finalUrl, listitem = li, isFolder = False)

def addNext(page):
    
    """Add a 'Next Page' button to a directory listing"""
    
    # construct url of next page
    u = sys.argv[0] + "?page=%s" % str(page)
    
    # initialise listitem object
    li = xbmcgui.ListItem('Next Page', iconImage = "DefaultFolder.png", thumbnailImage = "DefaultFolder.png")
    
    # set title of list item
    li.setInfo( type = "Video", infoLabels = { "Title" : 'Next Page' })
    
    # add listitem object to list
    xbmcplugin.addDirectoryItem(handle = __addonidint__, url = u, listitem = li, isFolder = True)
    
def endDir():
    xbmcplugin.endOfDirectory(handle = __addonidint__)

def playVideo(url):
    
    """Retrieve video details and play video
    
    Arguments:  url -- A string containing the url of the videos page on mmafighting.com"""
    
    # If the video is Vimeo (most likely) get the Vimeo URL
    if re.search(r'vimeo', url):
        videoUrl = cache.cacheFunction(vimeo.pull_video_url, url)
        success = True
    # If Ustream, the same
    elif re.search(r'ustream', url):
        videoUrl = cache.cacheFunction(ustream.pull_video_url, url)
        success = True
    else:
        success = False
    
    # add video details to listitem
    listitem = xbmcgui.ListItem(path = videoUrl)
    
    # play listitem
    xbmcplugin.setResolvedUrl(handle = __addonidint__, succeeded = success, listitem = listitem)  
