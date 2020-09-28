import os
import requests
import requests.auth


class GitHubClient:
    def __init__(self):
        self.s = requests.Session()
        self.s.auth = requests.auth.HTTPBasicAuth(os.getenv('GITHUB_USERNAME'), os.getenv('GITHUB_PASSWORD'))
        self.s.headers.update({'accept': 'application/vnd.github.v3+json'})

    def get_repositories(self):
        url = 'https://api.github.com/user/repos'
        while url is not None:
            response = self.s.get(url)
            response.raise_for_status()
            yield from response.json()
            url = None
            link_header = response.headers.get('link')
            links = [token.strip() for token in link_header.split(',')]
            for link in links:
                if 'rel="next"' in link:
                    url = link.split(';')[0].strip('<>')
                    break

    def call(self, url: str):
        response = self.s.get(url)
        response.raise_for_status()
        return response.json()


def main():
    client = GitHubClient()
    for repository in client.get_repositories():
        subscribed = False
        subscribers_url = repository.get('subscribers_url')
        subscribers = client.call(subscribers_url)
        for subscriber in subscribers:
            if subscriber.get('login') == os.getenv('GITHUB_USERNAME'):
                subscribed = True
                break
        if not subscribed:
            print(repository.get('full_name'))


if __name__ == '__main__':
    main()
