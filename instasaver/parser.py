#!/usr/local/bin/python3/
import argparse
import json
import re
import requests
from bs4 import BeautifulSoup

import config

# this code block belongs to George Gabolaev
GRAPH_SIDECAR_REG_ARGS = '"edge_sidecar_to_children":', '}}}]},"gatekeepers":'
GRAPH_SINGLE_MEDIA_REG_ARGS = '"shortcode_media":', 'racking_token'
FROM_TO_REGEX_PATTERN = r'(?<=({})).*(?=({}))'

def getMediaFromNode(node):
    return node['display_url'] if not node['is_video'] else node['video_url']


def graphSidecarSearch(jsonInDict):
    for edge in jsonInDict['edges']:
        yield getMediaFromNode(edge['node'])


def getContent(soup):
    script = soup.find('body').find('script', type='text/javascript').text
    try:
        if 'GraphSidecar' in script:
            foundedJSON = re.search(FROM_TO_REGEX_PATTERN.format(*GRAPH_SIDECAR_REG_ARGS), script)
            parsedNodes = json.loads(foundedJSON.group(0))
            urls = []
            for mediaURL in graphSidecarSearch(parsedNodes):
                urls.append(mediaURL)
            return urls
        else:
            foundedJSON = re.search(FROM_TO_REGEX_PATTERN.format(*GRAPH_SINGLE_MEDIA_REG_ARGS), script)
            parsedNode = json.loads(foundedJSON.group(0).replace(',"t', '}'))  # oh shit shame...
            return [getMediaFromNode(parsedNode)]
    except Exception as ex:
        pass
# end

def saveByURL(instagrmURL):
    pageHTML = requests.get(instagrmURL)
    soup = BeautifulSoup(pageHTML.content, 'lxml')
    return getContent(soup)
