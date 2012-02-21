# returns a video list or video from UStream
import urllib2
from elementtree import ElementTree as ET

def pull_video_url(url):
        
        vidID = url.replace('http://www.ustream.tv/recorded/', '')
        
        apiUrl = 'http://api.ustream.tv/xml/video/%s/getInfo?key=A5379FCD5891A9F9A029F84422CAC98C' % vidID
        
        # Build the page reuqest including setting the User Agent
        req  = urllib2.Request(apiUrl)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')

        # Open URL and read contents
        client = urllib2.urlopen(req)
        
        # retrieve data from podcast url
        data = client.read()
        # initialise the tree object using the returned data so it can be parsed
        tree = ET.fromstring(data)
        
        video = tree.find('results')
        print video
        # get episode url
        output_url = video.findtext('mp4Url')
        if not output_url:
            output_url = video.findtext('liveHttpUrl')
            
        #return video url
        return output_url
