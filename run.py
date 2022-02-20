from ConsoleWatcher import ConsoleWatcher
import json


config = json.load(open('config.json'))
target_urls = {'Xbox Series S': 'https://www.target.com/p/xbox-series-s-console/-/A-80790842',
               'Xbox Series X': 'https://www.target.com/p/xbox-series-x-console/-/A-80790841',
               'Gray Switch': 'https://www.target.com/p/nintendo-switch-with-gray-joy-con/-/A-77464002'}

watcher = ConsoleWatcher(target_urls, config)
watcher.check_availability()
