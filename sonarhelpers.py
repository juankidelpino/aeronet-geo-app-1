import requests

from helpers import print_error
from constants import JAP_SONAR_URL
from credentials import SONAR_USERNAME, SONAR_PASSWORD

def fetch_data_from_sonar(relative_url, params=None):
    """ Get sonar data from a specific url resource.
    
    Args:
        relative_url: {String} relative url to send GET request to
        params (dict): dict to send as query parameters
    
    Returns:
       (data, paginator) tuple made of the "data" key's value from the successful response (list or dictionary) 
       and the paginator dictionary.
    
    May raise exceptions for unsuccessful requests or error in sonar's json response
    """
    return _make_sonar_request('GET', relative_url, params=params)

def post_data_to_sonar(relative_url, payload):
    """ Post json data to Sonar to a specific url endpoint.
    
    Args:
        relative_url: {String} relative url to send POST request to
        payload: {object} json object to pass to the request's body as a JSON encoded string.
    
    Returns:
       (data, paginator) tuple made of the "data" key's value from the successful response (list or dictionary) 
       and the paginator dictionary.
    
    May raise exceptions for unsuccessful requests or error in sonar's json response
    """
    return _make_sonar_request('POST', relative_url, payload)

def patch_data_to_sonar(relative_url, payload):
    """ Patch json data to Sonar to a specific url endpoint.
    
    Args:
        relative_url: {String} relative url to send POST request to
        payload: {object} json object to pass to the request's body as a JSON encoded string.
    
    Returns:
       (data, paginator) tuple made of the "data" key's value from the successful response (list or dictionary) 
       and the paginator dictionary.
    
    May raise exceptions for unsuccessful requests or error in sonar's json response
    """
    return _make_sonar_request('PATCH', relative_url, payload)

def delete_data_from_sonar(relative_url):
    """ Make a DELETE request to a specific Sonar url endpoint.
    
    Args:
        relative_url: {string} relative url to send DELETE request to
    
    May raise exceptions for unsuccessful requests or error in sonar's json response
    """
    return _make_sonar_request("DELETE", relative_url)

def _make_sonar_request(method, relative_url, payload=None, params=None):
    """ Makes either a network request to the relative_url in Sonar's instance.
    
    Args:
        method: {string} the method of the network request (PUT, POST, GET, PATCH, DELETE)
        relative_url: {string} relative url to send GET request to
        payload: {object} json object to pass to the request's body as a JSON encoded string.
        params: {object} json object to pass to the request's query parameters
    
    Returns:
       (data, paginator) tuple made of the "data" key's value from the successful response (list or dictionary) 
       and the paginator dictionary with keys: 
        total_count
        total_pages
        current_page
        limit
    
    May raise exceptions for unsuccessful requests or error in sonar's json response
    """
    try:
        res = requests.request(method, '{0}{1}'.format(JAP_SONAR_URL, relative_url), json=payload, params=params, auth=(SONAR_USERNAME, SONAR_PASSWORD))
        res.raise_for_status()
    except requests.ConnectionError as e:
        print_error('{} request to Sonar endpoint {} failed due to connection error: {}'.format(method, relative_url, repr(e)))
        raise
    except requests.HTTPError as e:
        try:
            json_res = res.json()
        except ValueError:
            error = None
        else:
            error = json_res.get('error') if isinstance(json_res, dict) else None
        print_error('{} request to Sonar endpoint {} returned unsuccessful status code: {} and error message: {}'.format(method, 
                                                                                                                           relative_url, 
                                                                                                                           repr(e), 
                                                                                                                           error))
        raise
    else:
        try:
            json_res = res.json()
        except ValueError as e:
            print_error('{} request to Sonar endpoint {} found error getting json from response: {}'.format(method, 
                                                                                                            relative_url,
                                                                                                            repr(e)))
            raise
        else:
            return json_res['data'], json_res.get('paginator')