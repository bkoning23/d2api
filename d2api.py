import requests
import configparser
import zipfile
import os
import hashlib
from d2player import Destiny2Player
from d2db import d2db

class d2api:
    PLATFORM_URL = "https://www.bungie.net/Platform/Destiny2/"
    
    def __init__(self, apikey):
        self.api_key = apikey
        self.current_player = ""
        self.manifest_filename = ""
        self._update_manifest()
        self.get_triumph_info("58812229")

    def _get_request(self, url):
        headers = {"X-API-Key": self.api_key}
        #print(url)
        req = requests.get(url, headers=headers)
        return req

    def _update_manifest(self):
        url = self.PLATFORM_URL + "Manifest"
        world_url = (self._get_request(url)).json()['Response']['mobileWorldContentPaths']['en']

        base_file_name = world_url.split("/")[-1].split(".")[0]
        hash_string = base_file_name.split("_")[-1]
        zip_file_name = base_file_name + ".zip"
        sql_file_name = "manifest/" + base_file_name + ".sqlite3"
        
        if(os.path.exists(sql_file_name)):
            self.manifest_filename = sql_file_name
            return 0
            
        world_url = "https://www.bungie.net" + world_url
        r = requests.get(world_url)
        with open(zip_file_name, 'wb') as manifest:
            manifest.write(r.content)
        with zipfile.ZipFile(zip_file_name, 'r') as zip_ref:
            zip_ref.extractall("manifest")
        os.remove(zip_file_name)
        
        os.rename("manifest/" + base_file_name + ".content", sql_file_name)
        with open(sql_file_name, 'rb') as f:
            data = f.read()
            if(hash_string != (hashlib.md5(data).hexdigest())):
                os.remove(sql_file_name)
                return 1
        self.manifest_filename = sql_file_name

    def create_player(self, platform, name):
        member_data = self.get_membership_data(platform, name)
        player = Destiny2Player(member_data['displayName'], member_data['membershipType'], member_data['membershipId'])
        player.character_ids = self.get_character_ids(player.membership_type, player.membership_id)
        self.current_player = player

    def get_membership_data(self, platform, name):
        url = self.PLATFORM_URL + "SearchDestinyPlayer/{}/{}"
        url = url.format(platform, name)
        print(url)
        return ((self._get_request(url)).json()['Response'][0])

    def get_character_ids(self, platform, player_id):
        url = self.PLATFORM_URL + "{}/Profile/{}/?components=100"
        url = url.format(platform, player_id)
        print(url)
        return ((self._get_request(url)).json()['Response']['profile']['data']['characterIds'])

    def get_triumph_info(self, hash_id):
        db = d2db(self.manifest_filename)
        print(db.query("DestinyRecordDefinition", hash_id))
        return

    



    