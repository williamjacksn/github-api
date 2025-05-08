import github


def main():
    client = github.GitHubClient()
    for repository in client.get_repositories():
        repo_full_name = repository.get("full_name")
        for secret in client.get_secrets(repo_full_name):
            secret_name = secret.get("name")
            print(f"{repo_full_name}/{secret_name}")


if __name__ == "__main__":
    main()
