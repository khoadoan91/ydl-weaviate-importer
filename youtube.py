from yt_dlp import YoutubeDL
import requests
import xml.etree.ElementTree as ET
from html import unescape
URL = 'https://www.youtube.com/playlist?list=PLgRWqDITDkUn908s6EZA_NIX_-jTRahiP'

def download_playlist(playlist_url: str) -> (dict[str, any] | None):
  with YoutubeDL({
    'cookiefile': '~/Repos/Python/youtube-dl/youtube_cookies.txt'
  }) as ydl:
    # info = ydl.extract_info(playlist_url, download=False)
    # with open('playlist_sample2.json', 'w') as f:
    #   f.write(json.dumps(ydl.sanitize_info(info)))
    # return info
    return ydl.extract_info(playlist_url, download=False)


def download_transcript(url: str) -> str:
  response = requests.get(url)
  tree = ET.fromstring(response.content)
  texts = [unescape(e.text) for e in tree.findall('text')]
  return ' '.join(texts)