import requests
from json import dumps
from urllib.parse import urlparse
from urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning) # pylint: disable=no-member

class GLPIClient:
  __slots__ = [ 'url', 'app_token', 'user_token', 'session_token', 'headers', 'verify' ]

  class Util:
    @staticmethod
    def sanitize_url(url):
      pr = urlparse(url)
      return '{}://{}/'.format(pr.scheme, pr.netloc)
    
  def __init__(self, url, app_token, user_token, verify=True):
    self.url        = '{}apirest.php/'.format(GLPIClient.Util.sanitize_url(url))
    self.app_token  = app_token
    self.user_token = user_token
    self.verify     = verify
    self.headers    = {
      'App-Token': app_token,
      'Authorization': 'user_token: ' + user_token,
      'Content-Type': 'application/json'
    }

  def init_session(self):
    self.session_token = requests.get('{}initSession'.format(self.url), verify=self.verify, headers=self.headers).json()['session_token']
    self.headers['Session-Token'] = self.session_token

  def kill_session(self):
    if self.verify != None:
      self.session_token = None
      self.headers['Session-Token'] = None
      return requests.get('{}killSession'.format(self.url), verify=self.verify, headers=self.headers).json()
    raise Exception('Session token is not defined')

  def get_asset(self, name, id, params = {}):
    return requests.get('{}{}/{}'.format(self.url, name, id), params=params, verify=self.verify, headers=self.headers).json()

  def get_assets(self, name, text_params = {}, params = {}, max_range = 100):
    r0     = 0
    r1     = max_range
    p      = { 'searchText[{}]'.format(k): '^{}$'.format(v) for k, v in text_params.items() }
    result = []

    while True:
      params.update({ 'range': '{}-{}'.format(r0, r1) })
      p.update(params)
      _result = requests.get('{}{}'.format(self.url, name), params=p, verify=self.verify, headers=self.headers).json()
      result  = result + _result

      if len(_result) < max_range:
        break

      r0 = r1
      r1 = r1 + max_range

    return result


  def add_assets(self, name, assets):
    data = dumps({
      'input': assets
    })
    result = requests.post('{}{}'.format(self.url, name), data=data, verify=self.verify, headers=self.headers).json()
    return [ result ] if type(result) is dict else result

  def update_assets(self, name, assets):
    data = dumps({
      'input': assets
    })
    return requests.put('{}{}'.format(self.url, name), data=data, verify=self.verify, headers=self.headers).json()