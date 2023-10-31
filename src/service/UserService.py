import os
from db.tinydb import DB

class UserService:
  def __init__(self):
    self.DB = DB()
    
  def addUser(self, new_user_name: str):
    self.DB.addUser(new_user_name)
    
  def removeUser(self, user_name: str):
    self.DB.removeUser(user_name)

  def listUsers(self) -> [str]:
    return self.DB.listUsers()

  def isTheOwner(self, update) -> bool:
    user_name = update.message.from_user.name.lower()
    if user_name == os.environ.get('TELEGRAM_OWNER_NAME').lower():
        return True
    else:
        return False

  def isAllowedUser(self, update) -> bool:
    user_name = update.message.from_user.name.lower()
    if self.isTheOwner(update):
      return True
    else:
      return self.DB.isAllowedUser(user_name)