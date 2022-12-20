import github as g

def git_test():
    print("Git Check")
    # for repo in g.get_user().get_repos():
    #     print(repo.name)
        # repo.edit(has_wiki=False)
    g = Github("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")
    repo = g.get_repo("juankidelpino/ping-app-testing")
    contents = repo.get_contents("ping.txt")
    repo.update_file(contents.path, "Test on", "ping!", contents.sha, branch="main")
    
    return "Git Test Successful"

def reset_git_test():
    print("Resetting Git Test")

    g = Github("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")
    repo = g.get_repo("juankidelpino/ping-app-testing")
    contents = repo.get_contents("ping.txt")
    repo.update_file(contents.path, "Test off", "", contents.sha, branch="main")

    return "Git Test Reset"