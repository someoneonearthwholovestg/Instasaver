#!/usr/local/bin/python3/
import argparse
import json
import re
import webbrowser

import requests
from bs4 import BeautifulSoup


pageHTML = requests.get("https://www.instagram.com/p/BixTQqbgPT_/?taken-by=gal_gadot")
soup = BeautifulSoup(pageHTML.content, 'lxml')



print(soup)