from d2api import d2api
import configparser

config = configparser.ConfigParser()
config.read('config.ini')
APIKey = config['DEFAULT']['APIKey']

api = d2api(APIKey)
api.create_player(4, "Cookieking%231366")
print(api.current_player.character_ids)