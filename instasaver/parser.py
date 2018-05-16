#!/usr/local/bin/python3/
import argparse
import json
import re
import requests
from bs4 import BeautifulSoup

import config


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
    if 'GraphSidecar' in script:
        foundedJSON = re.search(FROM_TO_REGEX_PATTERN.format(*GRAPH_SIDECAR_REG_ARGS), script)
        parsedNodes = json.loads(foundedJSON.group(0))
        for mediaURL in graphSidecarSearch(parsedNodes):
            yield mediaURL
    else:
        foundedJSON = re.search(FROM_TO_REGEX_PATTERN.format(*GRAPH_SINGLE_MEDIA_REG_ARGS), script)
        parsedNode = json.loads(foundedJSON.group(0).replace(',"t', '}'))  # oh shit shame...
        yield getMediaFromNode(parsedNode)


def saveByURL(instagrmURL):
    try:
        print(instagrmURL)
        pageHTML = requests.get(instagrmURL)
        soup = BeautifulSoup(pageHTML.content, 'lxml')

        for url in getContent(soup):
            r = requests.get(url)
            with open('../cat3.jpg', 'wb') as f:  
                f.write(r.content)

        return True
    except Exception as ex:
        config.logFile(msg=ex)
        return False