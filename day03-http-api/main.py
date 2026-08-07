import json
from pathlib import Path

from github_client import GitHubAPIError, GitHubClient


BASE_DIR = Path(__file__).resolve().parent
DATA_FILE = BASE_DIR / "data" / "repository_snapshot.json"


def save_snapshot(data: dict) -> None:
    DATA_FILE.parent.mkdir(parents=True, exist_ok=True)

    with DATA_FILE.open("w", encoding="utf-8") as file:
        json.dump(
            data,
            file,
            ensure_ascii=False,
            indent=2,
        )


def main() -> None:
    owner = "addict-l"
    repository = "internship-growth"

    client = GitHubClient(timeout=10)

    try:
        repo = client.get_repository(owner, repository)

        print("\n========== 仓库信息 ==========")
        print(f"仓库：{repo['full_name']}")
        print(f"描述：{repo.get('description') or '暂无描述'}")
        print(f"默认分支：{repo['default_branch']}")
        print(f"公开仓库：{not repo['private']}")
        print(f"Stars：{repo['stargazers_count']}")
        print(f"Forks：{repo['forks_count']}")

        commits = client.get_latest_commits(
            owner,
            repository,
            limit=3,
        )

        print("\n========== 最近Commit ==========")

        for index, item in enumerate(commits, start=1):
            commit = item["commit"]
            message = commit["message"]
            author = commit["author"]

            print(f"\n{index}. {message}")
            print(f"   作者：{author.get('name', '未知')}")
            print(f"   时间：{author.get('date', '未知')}")
            print(f"   SHA：{item['sha'][:7]}")

        snapshot = {
            "repository": {
                "full_name": repo["full_name"],
                "description": repo.get("description"),
                "default_branch": repo["default_branch"],
                "stars": repo["stargazers_count"],
                "forks": repo["forks_count"],
            },
            "commits": [
                {
                    "sha": item["sha"],
                    "message": item["commit"]["message"],
                    "author": item["commit"]["author"].get("name"),
                    "date": item["commit"]["author"].get("date"),
                }
                for item in commits
            ],
        }

        save_snapshot(snapshot)
        print(f"\n数据已保存到：{DATA_FILE}")

    except GitHubAPIError as error:
        print(f"API调用失败：{error}")


if __name__ == "__main__":
    main()