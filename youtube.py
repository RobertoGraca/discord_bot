import urllib.request
import re

def get_link(args):
    url = f'https://www.youtube.com/results?search_query={args}'
    results = urllib.request.urlopen(url)    
    if(results.getcode() != 200):
        print(f'HTTP Error {results.getcode()}')
        return
    video_id = re.findall(r"watch\?v=(\S{11})", results.read().decode())[0]
    result_url = f'https://www.youtube.com/watch?v={video_id}'
    
    return result_url