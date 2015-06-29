import requests
# quiet warnings for self-signed certificates
requests.packages.urllib3.disable_warnings()

import json
import re

class ucclient():

  '''
   Setup a new UrbanCode client
  '''
  def __init__(self, base_url, user, password , debug=False):
    self._DEBUG = debug
    self.base_url = base_url
    self.auth_user = user
    self.auth_password = password
    self.session = requests.Session()

    # Login
    self.session.auth = ( self.auth_user, self.auth_password )
    self.session.verify = False
    response = self.session.get( self.base_url + '/security/user' )

    if response.status_code != requests.codes.ok:
     self.debug_reponse( response )
     raise Exception( 'Failed to login to UrbanCode' )

    cookies =  response.headers['set-cookie']

    # Figure out which client this is expecting a cookie named UC[BDR]_SESSION_KEY
    re_match = re.search('(UC[BDR]_SESSION_KEY)=(.{36});', cookies )
    if re_match:
      if self._DEBUG:
        print( " %s : %s " % ( re_match.group(1), re_match.group(2) ) )
      self.session.headers.update({re_match.group(1): re_match.group(2) })

  '''
    Get wrapper with the session
  '''
  def get( self, uri ):
    return self.session.get( self.base_url + uri, headers={'accept': 'application/json'} )

  '''
    Put wrapper
  '''
  def put( self, uri, data={}):
    return self.session.put( self.base_url + uri, data=data, headers={'accept': 'application/json', 'content-type': 'application/json'} )

  '''
   Helper for debugging the response objects
  '''
  def debug_reponse( self, response ):
    print( "         response.url: %s " % ( response.url ) )
    print( "    response.encoding: %s " % ( response.encoding ) )
    print( " response.status_code: %s " % ( response.status_code ) )
    print( "     response.headers: %s " % ( response.headers ) )
    print( "      session.cookies: %s " % ( self.session.cookies ) )
    print( "     response.headers: %s " % ( response.headers ) )
    print( "        response.text: %s " % ( response.text ) )
