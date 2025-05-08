import argparse
import datetime
import github


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("repo")
    return parser.parse_args()


def print_release_info(release_data: dict):
    version = release_data.get("tag_name")
    print(f"# {version}\n")
    date = datetime.datetime.strptime(
        release_data.get("published_at"), "%Y-%m-%dT%H:%M:%S%z"
    )
    print(f"{date.date()}\n")
    notes = release_data.get("body")
    notes = notes.replace("\r", "")
    if notes:
        if not notes.endswith("\n"):
            notes = f"{notes}\n"
        print(f"{notes}\n")


def main():
    args = parse_args()
    gh = github.GitHubClient()
    for release in gh.get_releases(args.repo):
        print_release_info(release)


if __name__ == "__main__":
    main()
