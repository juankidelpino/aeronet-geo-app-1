# import github
from github import Github
import credentials

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