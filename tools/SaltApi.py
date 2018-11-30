# coding: utf-8
import json
import requests

class SaltApi:
    def __init__(self,url):
        self.url = url
        self.username = 'admin'
        self.passwd = 'admin'
        self.headers = {
            'Content-type': 'application/json'
        }
        self.login_url = self.url + 'login'
        self.login_params = {
            'username' : self.username,
            'password' : self.passwd,
            'eauth' : 'pam'
        }
        self.token = self.get_data(self.login_url,self.login_params)['token']
        self.headers['X-Auth-Token'] = self.token
    
    def get_data(self,url,params):
        send_data = json.dumps(params)
        request = requests.post(url,data=send_data,headers=self.headers,verify=False)
        response = request.json()
        result = dict(response)
        return result['return'][0]
    
    def salt_command(self,target,method,arg=None):
        if arg:
            params = {
                'mode': 'sync',
                'client': 'local',
                'fun': method,
                'tgt': target,
                'arg': arg
            }
        else:
            params = {
                'mode': 'sync',
                'client': 'local',
                'fun': method,
                'tgt': target
            }
        result = self.get_data(self.url,params)
        return result['tgt']
