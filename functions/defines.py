import requests
import json

def getCreds() :
	""" Get creds required for use in the applications
	
	Returns:
		dictonary: credentials needed globally

	"""

	creds = dict() # dictionary to hold everything
	creds['access_token'] = 'EAA18eWDJ3hcBO6hZCAXFm4G5FUwjH8FbRr1iAPSQyv4r2O1gpISWopkvDcY1KVezZBclkus6oDSHbN6lEQU1vPcR0wDi4Gge94xGdkCcJh8GOoNkq1AgZB0ggru3yDRzUnPQznL0aHC2JIVL58DfWFZCjZC8mfeIUfUslPnbggvm2ExkDpKBKYzi78eg2UpkZCSZBmEOcsH' # access token for use with all api calls
	creds['client_id'] = '3796035453967895' # client id from facebook app IG Graph API Test
	creds['client_secret'] = 'fdca3d6ce0d185f27f3d015278419c74' # client secret from facebook app
	creds['graph_domain'] = 'https://graph.facebook.com/' # base domain for api calls
	creds['graph_version'] = 'v21.0' # version of the api we are hitting
	creds['endpoint_base'] = creds['graph_domain'] + creds['graph_version'] + '/' # base endpoint with domain and version
	creds['debug'] = 'no' # debug mode for api call
	creds['page_id'] = '112467505033594'
	creds['instagram_account_id'] = '17841456745468283'
	creds['ig_username'] = 'sevree.education'
	return creds

def makeApiCall( url, endpointParams, debug = 'no' ) :
	""" Request data from endpoint with params
	
	Args:
		url: string of the url endpoint to make request from
		endpointParams: dictionary keyed by the names of the url parameters


	Returns:
		object: data from the endpoint

	"""

	data = requests.get( url, endpointParams ) # make get request

	response = dict() # hold response info
	response['url'] = url # url we are hitting
	response['endpoint_params'] = endpointParams #parameters for the endpoint
	response['endpoint_params_pretty'] = json.dumps( endpointParams, indent = 4 ) # pretty print for cli
	response['json_data'] = json.loads( data.content ) # response data from the api
	response['json_data_pretty'] = json.dumps( response['json_data'], indent = 4 ) # pretty print for cli

	if ( 'yes' == debug ) : # display out response info
		displayApiCallData( response ) # display response

	return response # get and return content

def displayApiCallData( response ) :
	""" Print out to cli response from api call """

	print ("\nURL: ") # title
	print (response['url']) # display url hit
	print ("\nEndpoint Params: ") # title
	print (response['endpoint_params_pretty']) # display params passed to the endpoint
	print ("\nResponse: ") # title
	print (response['json_data_pretty']) # make look pretty for cli