import re
import sys
import csv
import base64

def write_report(data, file_name=None):
    """ Make csv file with each row in data.
    Args:
        data: {list} list of dictionaries with keys representing the columns.
        file_name: {str} the name of the resulting csv file. Defaults to "info.csv".
    """
    if not data:
        return
    with open(file_name or "info.csv", "w", newline='') as csvFile:
        field_names = data[0].keys()
        writer = csv.DictWriter(csvFile, fieldnames=field_names)
        writer.writeheader()
        for d in data:
            writer.writerow(d)

def print_error(*args, **kwargs):
    """ Wrapper for print() but uses sys.stderr instead of sys.stdout
    """
    print(*args, file=sys.stderr, **kwargs)

def account_number(name):
    """ Check if name has a 4 or 5 digit Sonar account number
    
    Args:
        name: {string} string to check if it has account number in it
    
    Returns:
        Account number as string if it has account number, None otherwise
    """
    match = re.search('(\D|\A|\W)+([0-9]{4,5})(\D|\b|\W|\Z)+', name or '')
    return match.group(2) if match else None

def b64_encode(*args, **kwargs):
    """ wrapper for base64.b64encode()
    """
    return base64.b64encode(*args, **kwargs)

def b64_decode(*args, **kwargs):
    """ wrapper for base64.b64decode()
    """
    return base64.b64decode(*args, **kwargs)