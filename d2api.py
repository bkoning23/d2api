import requests
import configparser
from Destiny2Player import Destiny2Player

xur_url = "https://www.bungie.net/Platform/Destiny/Advisors/Xur/"
player_id = "Cookieking#1366"

player_url = "https://www.bungie.net/Platform/Destiny2/"

#SearchDestinyPlayer/All/Cookieking%231366


def main():
    player = create_player("All", "Cookieking%231366")
    print(player.character_ids)
    
def get_request(url):
    config = configparser.ConfigParser()
    config.read('config.ini')
    APIKey = config['DEFAULT']['APIKey']
    headers = {"X-API-Key": APIKey}
    #print(url)
    req = requests.get(url, headers=headers)
    return req

def create_player(platform, name):
    member_data = get_membership_data(platform, name)
    player = Destiny2Player(member_data['displayName'], member_data['membershipType'], member_data['membershipId'])
    player.character_ids = get_character_ids(player.membership_type, player.membership_id)
    return (player)

def get_membership_data(platform, name):
    url = player_url + "SearchDestinyPlayer/{}/{}"
    url = url.format(platform, name)
    return ((get_request(url)).json()['Response'][0])

def get_character_ids(platform, player_id):
    url = player_url + "{}/Profile/{}/?components=100"
    url = url.format(platform, player_id)
    return ((get_request(url)).json()['Response']['profile']['data']['characterIds'])


main()
    