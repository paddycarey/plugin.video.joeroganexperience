import urllib
import urllib2
import re
import os
import sys
import StorageServer
import xbmcaddon
import xbmcplugin
import xbmcgui

from resources.lib import joerogan
from resources.lib import utils
from BeautifulSoup import BeautifulSoup

### get addon info
__addon__             = xbmcaddon.Addon()
__addonid__           = __addon__.getAddonInfo('id')
__addonidint__        = int(sys.argv[1])
# initialise cache object to speed up plugin operation
cache = StorageServer.StorageServer(__addonid__ + '-pages', 1)

class Main:

    def __init__(self):

        # parse script arguments
        params = utils.getParams()

        # Check if the url param exists
        try:
            url=urllib.unquote_plus(params["url"])
        except:
            
            try:
                # Get the current page number
                pageNum = int(params["page"])
            except:
                # Set page number to 1 if not dound
                pageNum = 1
            video_list = {}
            video_list = cache.cacheFunction(joerogan.pull_video_list, pageNum)
            # send each item to XBMC, mode 3 opens video
            for video in video_list:
                utils.addVideo(linkName = video['title'], url = video['url'], thumbPath = video['thumb'])
            # add a link to the Next Page
            utils.addNext(pageNum + 1)
            # We're done with the directory listing
            utils.endDir()
        else:
            utils.playVideo(url)


if __name__ == '__main__':
    
    # Main program
    Main()
        
