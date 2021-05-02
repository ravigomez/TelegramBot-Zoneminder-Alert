import os
import uuid
from requests import get

from service.ZoneMinderService import ZoneMinderService

class VideoService:
  def __init__(self):
    self.ZMService = ZoneMinderService()
    os.makedirs('./temp',exist_ok=True) 

  def videoGenerate(self, eventID: int) -> str:
    token = self.ZMService.getAccessToken()
    url = self.ZMService.BASE_URL + f'/index.php?view=view_video&eid={eventID}&token={token}'
    ramdomID = str(uuid.uuid4())
    videoPath = f"./temp/event_{eventID}_{ramdomID}.mp4"

    chunk_size = 256
    r = get(url, stream=True)
    with open(videoPath, "wb") as f:
      for chunk in r.iter_content(chunk_size=chunk_size):
        f.write(chunk)
    
    return videoPath

  def removeVideoFile(self, videoPath: str):
    try:
      os.remove(videoPath)
    except:
      pass
