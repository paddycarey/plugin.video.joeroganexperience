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
            try:
                guests = ''
                # Check if the Guests exist (some videos don't have any guests)
                guests_twit = div.findAll('a', href=re.compile('(http://www.twitter.com/.*)|(http://twitter.com/#!/.*)'))
                for count in range(len(guests_twit)):
                    guest = re.sub(r',|\ $', '', guests_twit[count].string) 
                    if count == 0:
                        guests = ' (' + guest
                    elif count == len(guests_twit)-1:
                        guests = guests + ' & ' + guest + ")"
                    else:
                        guests = guests + ', ' +  guest
                    if len(guests_twit)-1 == 0:
                        guests = guests + ')' 
            except:
                video['guests'] = ''
            else:
                video['guests'] = guests

        utils.log('Video found: %s' % video['title'])
        utils.log('URL: %s' % video['url'])
        utils.log('Thumb: %s' % video['thumb'])
        utils.log('Guests: %s' % video['guests'])
        videos.append(video)

    return videos
