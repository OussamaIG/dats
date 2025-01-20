import json
from defines import getCreds, makeApiCall
import sys

def getHashtagInfo(params):
    endpointParams = dict()
    endpointParams['user_id'] = params['instagram_account_id']
    endpointParams['q'] = params['hashtag_name']
    endpointParams['fields'] = 'id,name'
    endpointParams['access_token'] = params['access_token']

    url = params['endpoint_base'] + 'ig_hashtag_search'

    return makeApiCall(url, endpointParams, params['debug'])

def getHashtagMedia(params):
    endpointParams = dict()
    endpointParams['user_id'] = params['instagram_account_id']
    endpointParams['fields'] = 'id,children,caption,comment_count,like_count,media_type,media_url,permalink'
    endpointParams['access_token'] = params['access_token']

    url = params['endpoint_base'] + params['hashtag_id'] + '/' + params['type']

    return makeApiCall(url, endpointParams, params['debug'])

def getRecentlySearchedHashtags(params):
    endpointParams = dict()
    endpointParams['fields'] = 'id,name'
    endpointParams['access_token'] = params['access_token']

    url = params['endpoint_base'] + params['instagram_account_id'] + '/' + 'recently_searched_hashtags'

    return makeApiCall(url, endpointParams, params['debug'])

try:
    hashtag = sys.argv[1]
except:
    hashtag = 'sports'

params = getCreds()
params['hashtag_name'] = hashtag
hashtagInfoResponse = getHashtagInfo(params)

params['hashtag_id'] = hashtagInfoResponse['json_data']['data'][0]['id']

# Array to store all captions
all_captions = []

# Get top media captions
params['type'] = 'top_media'
hashtagTopMediaResponse = getHashtagMedia(params)

for post in hashtagTopMediaResponse['json_data']['data']:
    if 'caption' in post:
        all_captions.append(post['caption'])

# Get recent media captions
params['type'] = 'recent_media'
hashtagRecentMediaResponse = getHashtagMedia(params)

for post in hashtagRecentMediaResponse['json_data']['data']:
    if 'caption' in post:
        all_captions.append(post['caption'])

# Append to hashtagposts.json
try:
    with open('hashtagposts.json', 'r') as file:
        existing_data = json.load(file)
except FileNotFoundError:
    existing_data = []

existing_data.extend(all_captions)

with open('hashtagposts.json', 'w') as file:
    json.dump(existing_data, file, indent=4)

print("Captions saved to hashtagposts.json.")
