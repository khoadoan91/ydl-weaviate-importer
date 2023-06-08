
from weaviate_service import WeaviateService
from weaviate_types import YoutubeObject
from youtube import download_playlist, download_transcript

URL = 'https://www.youtube.com/playlist?list=PLgRWqDITDkUn908s6EZA_NIX_-jTRahiP'

weaviate = WeaviateService()
weaviate.create_youtube_schema()

response = download_playlist(URL)

data = [YoutubeObject(
    youtubeId=x["id"],
    title=x["title"],
    uploader=x["uploader"],
    uploaderId=x["uploader_id"],
    tags=x["tags"],
    description=x["description"],
    uploadDate=x["upload_date"],
    language=x["language"],
    playlistNames=[x["playlist_title"]],
    playlistIds=[x["playlist_id"]],
    transcriptionEnglish=download_transcript(next(lan["url"] for lan in x["automatic_captions"]["en-orig"] if lan["ext"] == 'srv1')),
    transcriptionVietnamese=download_transcript(next(lan["url"] for lan in x["automatic_captions"]["vi"] if lan["ext"] == 'srv1')),
    userAccount=response["uploader"],
    categories=x["categories"],
    chapters=[c["title"] for c in x["chapters"]] if x["chapters"] else []) for x in response["entries"]]

weaviate.batch_import(data, weaviate.weaviate_class)