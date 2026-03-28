import github


def main():
    gh = github.GitHubClient()

    print("Fetching repositories...")
    repos = list(gh.get_repositories())

    print(f"\nFound {len(repos)} repositories")
    print("\nChecking for open pull requests...\n")

    total_prs = 0
    repos_with_prs = []

    for repo in repos:
        full_name = repo["full_name"]
        url = f"https://api.github.com/repos/{full_name}/pulls"
        params = {"state": "open", "per_page": 100}

        try:
            prs = gh._get(url, params)

            if prs:
                total_prs += len(prs)
                repos_with_prs.append((full_name, prs))

                print(full_name)
                for pr in prs:
                    pr_number = pr["number"]
                    pr_title = pr["title"]
                    pr_url = pr["html_url"]
                    pr_author = pr["user"]["login"]
                    created_at = pr["created_at"][:10]

                    print(f"  #{pr_number}: {pr_title}")
                    print(f"    Author: {pr_author} | Created: {created_at}")
                    print(f"    URL: {pr_url}")
                print()
        except Exception as e:
            print(f"  Error fetching PRs for {full_name}: {e}")

    print()
    print("=" * 60)
    pr_plural = "s"
    if total_prs == 1:
        pr_plural = ""
    repo_plural = "ies"
    if len(repos_with_prs) == 0:
        repo_plural = "y"
    print(
        f"Summary: {total_prs} open pull request{pr_plural} across {len(repos_with_prs)} repositor{repo_plural}"
    )
    print("=" * 60)


if __name__ == "__main__":
    main()
