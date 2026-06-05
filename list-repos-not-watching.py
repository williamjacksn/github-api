import github


def main() -> None:
    client = github.GitHubClient()
    for repository in client.get_repositories():
        subscribed = False
        for subscriber in client.get_subscribers(repository["full_name"]):
            if subscriber["login"] == client.username:
                subscribed = True
                break
        if not subscribed:
            print(repository.get("full_name"))


if __name__ == "__main__":
    main()
