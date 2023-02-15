import github


def main():
    client = github.GitHubClient()
    for repository in client.get_repositories():
        subscribed = False
        subscribers_url = repository.get('subscribers_url')
        subscribers = client._get(subscribers_url)
        for subscriber in subscribers:
            if subscriber.get('login') == client.username:
                subscribed = True
                break
        if not subscribed:
            print(repository.get('full_name'))


if __name__ == '__main__':
    main()
