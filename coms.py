# import github
from github import Github
import credentials
from gcloud import storage

bearer_token = credentials.GITHUB_BEARER_TOKEN

def git_test():
    print("Git Check")

    g = Github(bearer_token)
    repo = g.get_repo("juankidelpino/ping-app-testing")
    contents = repo.get_contents("ping.txt")
    repo.update_file(contents.path, "Test on", "ping!", contents.sha, branch="main")
    
    return "Git Test Successful"

def reset_git_test():
    print("Resetting Git Test")

    g = Github(bearer_token)
    repo = g.get_repo("juankidelpino/ping-app-testing")
    contents = repo.get_contents("ping.txt")
    repo.update_file(contents.path, "Test off", "", contents.sha, branch="main")

    return "Git Test Reset"

def upload_results(content):

    g = Github(bearer_token)
    repo = g.get_repo("juankidelpino/ping-app-testing")
    repo.create_file('aeronet_output.csv', 'committed from app', content.to_csv())

    return "Results Uploaded to Github."
    
def upload_to_bucket(blob_name, path_to_file, bucket_name):
    """ Upload data to a bucket"""
     
    # Explicitly use service account credentials by specifying the private key
    # file.
    storage_client = storage.Client.from_service_account_json(
        'creds.json')

    #print(buckets = list(storage_client.list_buckets())

    bucket = storage_client.get_bucket(bucket_name)
    blob = bucket.blob(blob_name)
    blob.upload_from_filename(path_to_file)
    
    #returns a public url
    return blob.public_url