import os
import requests


class GitHubClient:
    def __init__(self):
        self.token = os.getenv('GITHUB_TOKEN')
        self.s = requests.Session()
        self.s.headers.update({
            'accept': 'application/vnd.github+json',
            'authorization': f'Bearer {self.token}',
            'x-github-api-version': '2022-11-28',
        })

    def _get(self, url: str, params: dict= None):
        response = self.s.get(url, params=params)
        response.raise_for_status()
        return response.json()

    def _put(self, url: str, json_data: dict):
        response = self.s.put(url, json=json_data)
        response.raise_for_status()

    def get_actions_permissions_workflow(self, repo: str):
        url = f'https://api.github.com/repos/{repo}/actions/permissions/workflow'
        response = self._get(url)
        return response

    def set_actions_permissions_workflow(self, repo: str, default_workflow_permissions: str, can_approve_pull_request_reviews: bool):
        url = f'https://api.github.com/repos/{repo}/actions/permissions/workflow'
        json_data = {
            'default_workflow_permissions': default_workflow_permissions,
            'can_approve_pull_request_reviews': can_approve_pull_request_reviews,
        }
        self._put(url, json_data)

    def get_branches(self, repo: str):
        url = f'https://api.github.com/repos/{repo}/branches'
        response = self._get(url)
        yield from response

    def get_releases(self, repo: str):
        url = f'https://api.github.com/repos/{repo}/releases'
        params = {
            'page': 1,
            'per_page': 100,
        }
        has_more = True
        while has_more:
            response = self._get(url, params)
            yield from response
            if response:
                params.update({
                    'page': params.get('page') + 1
                })
            else:
                has_more = False


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
