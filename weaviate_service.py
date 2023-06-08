from dotenv import load_dotenv
from weaviate import AuthApiKey, Client
from weaviate.util import generate_uuid5
from os import environ
from weaviate_types import YoutubeObject
load_dotenv()

class WeaviateService:
  def __init__(self) -> None:
    api_key = environ.get('WEAVIATE_API_KEY')
    weaviate_url = environ.get('WEAVIATE_URL')
    auth_config = AuthApiKey(api_key)
    self.client = Client(weaviate_url, auth_config)
    self.weaviate_class = "Youtube"

  def create_youtube_schema(self) -> None:
    if self.client.schema.exists(self.weaviate_class):
      return
    youtube_schema = {
      "class": self.weaviate_class,
      "description": "My favorite Youtube video",
      "invertedIndexConfig": {
          "stopwords": {
              "preset": "en"
          }
      },
      "moduleConfig": {},
      "properties": [
        {
            "dataType": ["text"],
            "tokenization": "field",
            "name": "youtubeId"
        },
        {
            "dataType": ["text"],
            "name": "title"
        },
        {
            "dataType": ["text"],
            "tokenization": "field",
            "name": "uploader"
        },
        {
            "dataType": ["text"],
            "tokenization": "field",
            "name": "uploaderId"
        },
        {
            "dataType": ["text[]"],
            "name": "tags"
        },
        {
            "dataType": ["text"],
            "name": "description"
        },
        {
            "dataType": ["date"],
            "name": "uploadDate"
        },
        {
            "name": "language",
            "dataType": ["text[]"],
            "tokenization": "field"
        },
        {
            "name": "playlistNames",
            "dataType": ["text[]"],
            "tokenization": "field"
        },
        {
            "name": "playlistIds",
            "dataType": ["text[]"],
            "tokenization": "field"
        },
        {
            "name": "transcriptionEnglish",
            "dataType": ["text"]
        },
        {
            "name": "transcriptionVietnamese",
            "dataType": ["text"]
        },
        {
            "name": "userAccount",
            "dataType": ["text"],
            "tokenization": "field"
        },
        {
            "name": "categories",
            "dataType": ["text[]"]
        },
        {
            "name": "chapters",
            "dataType": ["text[]"]
        }
      ],
      "vectorizer": "text2vec-openai"
    }
    self.client.schema.create_class(youtube_schema)

  def batch_import(self, data: list[YoutubeObject], class_name: str) -> None:
    self.client.batch.configure(batch_size=500)
    with self.client.batch as batch:
      for item in data:
        batch.add_data_object(item, class_name, uuid=generate_uuid5(item.youtubeId))

