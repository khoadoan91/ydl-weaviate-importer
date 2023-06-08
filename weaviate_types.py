from dataclasses import dataclass

@dataclass(frozen=True)
class YoutubeObject(dict):
  youtubeId: str
  title: str
  uploader: str
  uploaderId: str
  tags: list[str]
  description: str
  uploadDate: str
  language: list[str]
  playlistNames: list[str]
  playlistIds: list[str]
  transcriptionEnglish: str
  transcriptionVietnamese: str
  userAccount: str
  categories: list[str]
  chapters: list[str]