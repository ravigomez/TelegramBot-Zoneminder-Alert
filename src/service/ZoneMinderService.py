import requests
import json
import os
from datetime import datetime, timedelta

from db.tinydb import DB
from service.UserService import UserService

class ZoneMinderService:
  def __init__(self):
    super().__init__()
    self.DB = DB()
    self.BASE_URL = os.environ.get('ZONEMINDER_URL')
    self.ZM_USER = os.environ.get('ZONEMINDER_USER')
    self.ZM_PASS = os.environ.get('ZONEMINDER_PASSWORD')

  def getAccessToken(self) -> str:
    token_data = self.DB.getToken()
    if not token_data:
      token_data = self.__generateNewAccessTokenData()
    else:
      token = token_data['access_token']
      url = self.BASE_URL + f'/api/events/0.json?token={token}'
      resp = requests.get(url)
      if resp.status_code != 200:
        token_data = self.__generateNewAccessTokenData()
        
      #TODO: check if the token is valid
      #TODO: try to renovate using refresh token
      #TODO: try to renovate using username and password

    return token_data['access_token']

  def __generateNewAccessTokenData(self):
    url = self.BASE_URL + f'/api/host/login.json'
    payload = {"user": self.ZM_USER, "pass": self.ZM_PASS}
    resp = requests.post(url, data=payload)
    
    if resp.status_code == 200:
      token_data = resp.json()
      self.DB.saveToken(token_data)
    else:
        raise Exception("Unable to get new token from ZoneMinder." + resp.data.name)
    
    return token_data

  def getEvent(self, eventID):
    while(True):
      url = self.BASE_URL + f'/api/events/{eventID}.json'
      try:
        resp = requests.get(url)

        if not resp.success and resp.data.message == "Invalid event":
          break
      except:
        break
  
  def getLatestEventsIDs(self, user_name: str, limit_of_time: bool) -> [int]:
    events = []
    page = 1
    token = self.getAccessToken()
    latestEventID = self.DB.getLatestEventID(user_name)
    while(True):
      url = self.BASE_URL + f'/api/events.json?page={page}&limit=30&sort=StartTime&direction=desc&token={token}'
      try:
        resp = requests.get(url)
        if resp.status_code == 200:
          data = resp.json()
          time_limit = datetime.now() - timedelta(hours=24)
          for e in data['events']:
            currentEventID = int(e['Event']['Id'])
            if currentEventID <= latestEventID: break
            if limit_of_time and datetime.fromisoformat(e['Event']['StartTime']) < time_limit: break
            events.append(currentEventID)
        else:
          break
        page += 1    
      except:
        break
        raise Exception("Error")
    
    return events
  
  def saveLatestEventID(self, user_name: str, eventID: int):
    self.DB.saveLatestEventID(user_name, eventID )

  def createVideoFile():
    pass
    