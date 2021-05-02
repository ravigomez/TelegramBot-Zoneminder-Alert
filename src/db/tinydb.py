
import os

from tinydb import TinyDB, Query, where
from tinydb.operations import delete

class DB():
  def __init__(self):
    os.makedirs('./localDB',exist_ok=True) 
    self.db = TinyDB('./localDB/db.json')

  def addUser(self, new_user_name: str):
    table = self.db.table('Users')
    Users = Query()
    table.upsert({'user_name': new_user_name }, Users.user_name == new_user_name )
  
  def isAllowedUser(self, user_name: str) -> bool:
    table = self.db.table('Users')
    user = table.get(Query().user_name == user_name)
    if user != None:
        return True
    else:
        return False

  def removeUser(self, user_name: str):
    if user_name != '':
      table = self.db.table('Users')
      user = table.get(Query().user_name == user_name)
      table.remove(doc_ids=[user.doc_id])

  def listUsers(self) -> [str]:
    users = self.db.table('Users')
    userList = []
    for u in users:
      userList.append(u["user_name"])
    return userList
    
  def getToken(self):
    table = self.db.table('Config')
    if len(table.all()) == 0:
      token_data = None
    else:
      token_data = table.get(Query().key == 'ZM_access_token')['value']
    return token_data

  def saveToken(self, token_data):
    table = self.db.table('Config')
    Config = Query()
    table.upsert({'key': 'ZM_access_token', 'value': token_data}, Config.key == 'ZM_access_token' )

  def getLatestEventID(self, user_name: str) -> int:
    try:
      table = self.db.table('LatestEventID')
      if len(table.all()) == 0:
        latesteEventID = os.environ.get('ZONEMINDER_EVENT_ID_INITIAL')
      else:
        data = table.get(Query().user_name == user_name)
        if data:
          latesteEventID = table.get(Query().user_name == user_name)['latesteEventID']
        else:
          latesteEventID = os.environ.get('ZONEMINDER_EVENT_ID_INITIAL')
          
      return int(latesteEventID)
    except:
      raise Exception("Erro while traying to getLatestEventID")

  def saveLatestEventID(self, user_name: str, latesteEventID: int):
    table = self.db.table('LatestEventID')
    LatestEventID = Query()
    table.upsert({'user_name': user_name, 'latesteEventID': latesteEventID}, LatestEventID.user_name == user_name )
    
    

