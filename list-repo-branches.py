import github

def main():
    client = github.GitHubClient()
    for repository in client.get_repositories():
        repo_full_name = repository.get('full_name')
        for branch in client.get_branches(repo_full_name):
            branch_name = branch.get('name')
            if branch_name not in ['main', 'master']:
                print(f'{repo_full_name}/{branch_name}')


if __name__ == '__main__':
    main()
