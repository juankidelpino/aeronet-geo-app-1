import sonarhelpers
import constants

# SONAR_ACCOUNT_STATUS_ID_ACTIVE_SET = {2, 5, 9, 12}
SONAR_ACCOUNT_STATUS_ACTIVE= 2
SONAR_ACCOUNT_STATUS_ID_CLOSED_SET = {4, 6}
_ACCOUNT_TYPE_ID_TO_NAME_MAP = {}

def get_all_accounts(only_active=False, only_type_ids=None):
    """ Return a list of all Sonar accounts.
    
    Args:
        only_active: {bool} whether only to return active accounts. Defaults to False. Active accounts
                            is defined as all those accounts that are not closed.
        only_type_ids: {set} set of ids for the account types to return. Defaults to None and returns
                            all account types
    
    May raise request errors.
    """
    all_accounts = _get_all_entities("/accounts")
    to_return = all_accounts
    if only_active:
        to_return = list(filter(lambda x: x["account_status_id"] == SONAR_ACCOUNT_STATUS_ACTIVE, all_accounts))
    
    # filter types if needed
    if only_type_ids:
        to_return = list(filter(lambda x: x["account_type_id"] in only_type_ids, to_return))
    
    if constants.JAP_TESTING_FLAG:
        return list(filter(lambda x: x["id"] == 17, to_return))
    
    to_return = to_return[:200]

    return to_return

def _get_all_entities(relative_url):
    """ Fetch all entities of a type from Sonar.
    
    Args:
        relative_url: the relative url of the resource to fetch.
    
    Returns:
        list of resources fetched as returned by Sonar
    
    May raise request errors.
    """
    all_entities = []
    finished = False
    page = 1
    while not finished:
        url = '{}?limit=100&page={}'.format(relative_url, page)
        print("Fetching " + url)
        entities, paginator = sonarhelpers.fetch_data_from_sonar(url)
        all_entities.extend(entities)
        if paginator["total_pages"] == page:
            finished = True
        else:
            page += 1
    return all_entities

# def get_account_data_service(account_id):
#     """ Fetches an account's data service. It does this by fetching all services from account
#     and then fetching the details of each one and finding the first one that has the "data_service" flag
    
#     Args:
#         account_id (int): the id of the Sonar account
    
#     Reeturns:
#         (service, current_price) tuple of dictionary of the Sonar service that is a data service and
#         the current price the account is paying for this service. None if no data service was found
#     """
#     services, pag = get_account_services(account_id)
#     for s in services:
#         overriden_price = float(s["price_override"]) if s["price_override"] else None
#         details = get_service_details(s["id"])
#         price = details["amount"]
#         if details["data_service"]:
#             return details, overriden_price or price
    
#     return None, None

def get_account_services(account_id):
    """ Fetch from Sonar the services tied to the account.
    
    Args:
        account_id: the Sonar id of the account
    
    Returns:
        (services, paginator) tuple of list of Service item dictionary objects as returned by Sonar, 
        and the paginator dictionary.
    """
    return sonarhelpers.fetch_data_from_sonar('/accounts/{}/services?limit=100&page=1'.format(account_id))

def fetch_account_custom_fields(account_id):
    """ Fetches an account's custom fields
    
    Args:
        account_id: {int} the account's Sonar ID
    
    Returns:
        List of dictionaries representing custom fields. Each dict has a "data" and "custom_field_id" key.
    
    May raise FailedRequest error.
    """
    data, _ = sonarhelpers.fetch_data_from_sonar("/entity_custom_fields/account/{}".format(account_id))
    return data

def get_all_services():
    """ Fetch all Sonar services
    
    Returns:
        list of Service item dictionary objects as returned by Sonar
    """
    return _get_all_entities('/system/services')

def fetch_account(account_id):
    """ Fetch a specific Sonar account.
    
    Args:
        account_id: {int} the id of the Sonar account to fetch
    
    Returns:
        JSON object representing the account as returned by Sonar
    
    May raise FailedRequest error.
    """
    data, _ = sonarhelpers.fetch_data_from_sonar("/accounts/{}".format(account_id))
    return

def fetch_account_addresses(account_id):
    """ Fetch addresses of an account
    Args
        account_id (int): the id of the Sonar account
    
    Returns:
        Paginated list of addresses, if any.
    """
    relative_url = f"/accounts/{account_id}/addresses"
    data, _ = sonarhelpers.fetch_data_from_sonar(relative_url)
    return data