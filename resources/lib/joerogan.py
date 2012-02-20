import urllib
import urllib2
import re
import os
import traceback
from BeautifulSoup import BeautifulSoup
import resources.lib.utils as utils

def pull_video_list(page_no):
    """
    Gets the list of thumbnails, video URLs and titles from the video site and display the list

    @param string url - Main URL of uStream page (without page number)
    @param int page_no - Page number to get

    @returns dictionary
    """     
    
    # Get the page number and add it to the URL (to allow moving through the video pages)
    url = "http://blog.joerogan.net" + "/page/" + str(page_no)

    videos = []

    # Create a new soup instance and assign a video list html to a variable
    soup = BeautifulSoup(utils.getHtml(url))

    # Get all the divs with the podcast content
    result = soup.find('tr', id='bodyrow').find('td', id='middle').findAll('div', id=re.compile('post-\d+'))

    # For each div
    for r in result:
        
        video = {}
        
        # Get the title
        video['title'] = r.find('div', 'post-headline').h2.a.string

        try:
            # Get the main divs
            div = r.find('div', 'post-bodycopy clearfix')
        except:
            print traceback.format_exc()
        else:
            try:
                # Get the video URL
                video['url'] = div.center.a['href']
            except:
                video['url'] = r.find('div', 'post-bodycopy clearfix').center.iframe['src']
            try:
                # Get the thumbnail
                video['thumb'] = div.center.img['src']
            except:
                video['thumb'] = ''

        utils.log('Video found: %s' % video['title'])
        utils.log('URL: %s' % video['url'])
        utils.log('Thumb: %s' % video['thumb'])
        if not re.search(r"(ustream)|(vimeo)", video['url']) is None:
            videos.append(video)

    return videos
