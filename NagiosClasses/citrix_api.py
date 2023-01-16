#!/usr/bin/python3

import requests

class CitrixApi:
    def __init__(self, client_id, client_secret, customer_id):
        self.data = {"grant_type": "client_credentials",
                "client_id": client_id,
                "client_secret": client_secret,
        }
        self.headers = {
            'Citrix-CustomerId': customer_id,
            'Citrix-Locale': 'en-US',
            'accept': '*/*',
        }
    
    def get_token(self, put_in_header = True):
        url = 'https://api-us.cloud.com/cctrustoauth2/root/tokens/clients'
        response = requests.post(url, data=self.data)
        if response.status_code != 200:
            raise Exception('Error getting token... Status code {response.status_code}'.format(response=response))
        self.token = response.json()['access_token']
        if put_in_header:
            self.headers.update({"Authorization": 'CwsAuth bearer= {self.token}'.format(self=self)})
            return 0
        else:
            return self.token

    def get_info(self, url, headers={}):
        try:
            self.headers.update(headers)
            return requests.get(url, headers=self.headers).json()
        except Exception as e:
            raise Exception(e)

    def get_my_instance_id(self, put_in_header = True):
        try:
            url = 'https://api-us.cloud.com/cvadapis/me'
            instance_id = self.get_info(url, self.headers)["Customers"][0]["Sites"][0]["Id"]
            if put_in_header:
                self.headers.update({"Citrix-InstanceId": instance_id})
                return 0
            else:
                return instance_id
        except Exception as e:
            raise Exception(e)