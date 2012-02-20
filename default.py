import urllib
import urllib2
import re
import os
import xbmcplugin
import xbmcgui

from resources.lib import joerogan
from resources.lib import utils

from BeautifulSoup import BeautifulSoup

class Main:

    def __init__(self):

        params = utils.getParams()

        # Check if the url param exists
        try:
            url=urllib.unquote_plus(params["url"])
        except:
            # Set the default page number
            try:
                pageNum = int(params["page"])
            except:
                pageNum = 1
            video_list = {}
            video_list = joerogan.pull_video_list(pageNum)
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
        
