import json
from defines import getCreds, makeApiCall

def getUserMedia(params, pagingUrl=''):
    """ Get users media

    API Endpoint:
        https://graph.facebook.com/{graph-api-version}/{ig-user-id}/media?fields={fields}&access_token={access-token}

    Returns:
        object: data from the endpoint
    """

    endpointParams = dict()  # parameter to send to the endpoint
    endpointParams['fields'] = 'id,caption,media_type,media_url,permalink,thumbnail_url,timestamp,username'  # fields to get back
    endpointParams['access_token'] = params['access_token']  # access token

    if pagingUrl == '':  # get first page
        url = params['endpoint_base'] + params['instagram_account_id'] + '/media'  # endpoint url
    else:  # get specific page
        url = pagingUrl  # endpoint url

    return makeApiCall(url, endpointParams, params['debug'])  # make the API call


params = getCreds()  # get creds
params['debug'] = 'no'  # set debug

# List to store media data
media_data = []

# Initialize pagination variables
pagingUrl = ''
page_number = 1

while True:
    print(f"\n\n\n\t\t\t >>>>>>>>>>>>>>>>>>>> PAGE {page_number} <<<<<<<<<<<<<<<<<<<<\n")  # display page heading

    # Get media from API (passing pagingUrl if it's not the first page)
    response = getUserMedia(params, pagingUrl)

    # Iterate through each post on the current page
    for post in response['json_data']['data']:
        # Safely get caption (if available)
        caption = post.get('caption', 'No caption available')  # Use default text if 'caption' is missing

        post_data = {
            "link_to_post": post['permalink'],
            "caption": caption,
            "media_type": post['media_type'],
            "timestamp": post['timestamp']
        }
        # Append the post data to the list
        media_data.append(post_data)

    # Check if there is a next page (pagination)
    if 'paging' in response['json_data'] and 'next' in response['json_data']['paging']:
        # Get the URL for the next page of posts
        pagingUrl = response['json_data']['paging']['next']
        page_number += 1
    else:
        # No more pages available, break the loop
        break

# Save the media data to a JSON file
with open('media_data.json', 'w') as json_file:
    json.dump(media_data, json_file, indent=4)

print("\nAll pages have been processed and saved to 'media_data.json'.")
