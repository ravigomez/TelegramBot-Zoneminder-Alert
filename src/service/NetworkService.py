from requests import get

class NetworkService:
  def __init__(self):
    pass
  def getPublicIP(self) -> str:
    try:
        ip = get('https://api.ipify.org').text
    except:
        update.message.reply_text('ERROR while trying to get Public IP')
    return ip