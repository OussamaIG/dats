import json
from defines import getCreds, makeApiCall

def getUserMedia(params, pagingUrl=''):
    """ Get users media (pages of media) """
    endpointParams = dict()  # parameter to send to the endpoint
    endpointParams['fields'] = 'id,caption,media_type,media_url,permalink,thumbnail_url,timestamp,username'  # fields to get back
    endpointParams['access_token'] = params['access_token']  # access token

    if pagingUrl == '':  # get first page
        url = params['endpoint_base'] + params['instagram_account_id'] + '/media'  # endpoint URL
    else:  # get specific page
        url = pagingUrl  # endpoint URL

    return makeApiCall(url, endpointParams, params['debug'])  # make the API call


def getMediaInsights(params):
    """ Get insights for a specific media id """
    endpointParams = dict()  # parameter to send to the endpoint
    endpointParams['metric'] = params['metric']  # fields to get back
    endpointParams['access_token'] = params['access_token']  # access token

    url = params['endpoint_base'] + params['latest_media_id'] + '/insights'  # endpoint URL

    return makeApiCall(url, endpointParams, params['debug'])  # make the API call


def getUserInsights(params):
    """ Get insights for a user's account """
    endpointParams = dict()  # parameter to send to the endpoint
    endpointParams['metric'] = 'impressions,reach,accounts_engaged,follows_and_unfollows'  # fields to get back
    endpointParams['period'] = 'day'  # period
    endpointParams['metric_type'] = 'total_value'  # 
    endpointParams['access_token'] = params['access_token']  # access token

    url = params['endpoint_base'] + params['instagram_account_id'] + '/insights'  # endpoint URL

    return makeApiCall(url, endpointParams, params['debug'])  # make the API call


params = getCreds()  # Get credentials
params['debug'] = 'no'  # Set debug to no

all_posts = []  # List to store all posts

# Loop through all pages of media
pagingUrl = ''
while pagingUrl is not None:
    # Get media data from the API (including pagination)
    response = getUserMedia(params, pagingUrl)

    # Loop through all posts on the current page
    for post in response['json_data']['data']:
        post_data = {
            "id": post['id'],
            "link_to_post": post['permalink'],
            "caption": post.get('caption', 'No Caption'),  # Handle missing caption field
            "media_type": post['media_type'],
            "timestamp": post['timestamp']
        }
        
        # Store the latest media ID to get insights
        params['latest_media_id'] = post['id']

        # Check the media type and set the appropriate metrics for insights
        if post['media_type'] == 'VIDEO':
            params['metric'] = 'likes,comments,shares,reach,saved,plays'
        else:
            params['metric'] = 'likes,comments,shares,impressions,reach,saved'

        # Get insights for this specific post
        insights_response = getMediaInsights(params)

        # Add the insights data to the post
        post_data['insights'] = []
        for insight in insights_response['json_data']['data']:
            post_data['insights'].append({
                "title": insight['title'],
                "period": insight['period'],
                "value": insight['values'][0]['value']
            })

        # Append the post data with insights to the list
        all_posts.append(post_data)

        # Print progress after each post
        print(f"Processed post {post['id']} - {post['media_type']} - {post['timestamp']}")

    # Check if there is a next page of posts
    if 'paging' in response['json_data'] and 'next' in response['json_data']['paging']:
        pagingUrl = response['json_data']['paging']['next']
    else:
        pagingUrl = None  # No more pages, stop the loop

# Save the posts with insights to a JSON file
with open('posts_with_insights.json', 'w') as outfile:
    json.dump(all_posts, outfile, indent=4)

print(f"Total posts with insights collected: {len(all_posts)}")
