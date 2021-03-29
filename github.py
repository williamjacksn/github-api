import os
import requests


class GitHubClient:
    def __init__(self):
        self.username = os.getenv('GITHUB_USERNAME')
        self.s = requests.Session()
        self.s.auth = requests.auth.HTTPBasicAuth(self.username, os.getenv('GITHUB_PASSWORD'))
        self.s.headers.update({'accept': 'application/vnd.github.v3+json'})

    def call(self, url: str):
        response = self.s.get(url)
        response.raise_for_status()
        return response.json()

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

    def get_secrets(self, repo_full_name):
        url = f'https://api.github.com/repos/{repo_full_name}/actions/secrets'
        response = self.s.get(url)
        response.raise_for_status()
        yield from response.json().get('secrets', [])
