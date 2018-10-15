import requests
import configparser
from d2player import Destiny2Player

class d2api:
    xur_url = "https://www.bungie.net/Platform/Destiny/Advisors/Xur/"
    player_id = "Cookieking#1366"

    player_url = "https://www.bungie.net/Platform/Destiny2/"

    #SearchDestinyPlayer/All/Cookieking%231366
    
    def __init__(self, apikey):
        self.api_key = apikey
        self.current_player = ""

    def get_request(self, url):
        headers = {"X-API-Key": self.api_key}
        #print(url)
        req = requests.get(url, headers=headers)
        return req

    def create_player(self, platform, name):
        member_data = self.get_membership_data(platform, name)
        player = Destiny2Player(member_data['displayName'], member_data['membershipType'], member_data['membershipId'])
        player.character_ids = self.get_character_ids(player.membership_type, player.membership_id)
        self.current_player = player

    def get_membership_data(self, platform, name):
        url = self.player_url + "SearchDestinyPlayer/{}/{}"
        url = url.format(platform, name)
        print(url)
        return ((self.get_request(url)).json()['Response'][0])

    def get_character_ids(self, platform, player_id):
        url = self.player_url + "{}/Profile/{}/?components=100"
        url = url.format(platform, player_id)
        return ((self.get_request(url)).json()['Response']['profile']['data']['characterIds'])



    