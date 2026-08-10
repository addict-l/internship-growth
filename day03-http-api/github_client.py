from typing import Any

import requests


class GitHubAPIError(Exception):
    """GitHub API 调用失败。"""


class GitHubClient:
    """负责调用 GitHub REST API。"""

    BASE_URL = "https://api.github.com"

    def __init__(self, timeout: int = 10) -> None:
        self.timeout = timeout

        self.session = requests.Session()
        self.session.headers.update(
            {
                "Accept": "application/vnd.github+json",
                "User-Agent": "internship-growth-learning",
            }
        )

    def get_repository(
        self,
        owner: str,
        repository: str,
    ) -> dict[str, Any]:
        """获取指定仓库的信息。"""
        url = f"{self.BASE_URL}/repos/{owner}/{repository}"

        try:
            response = self.session.get(
                url,
                timeout=self.timeout,
            )

            if response.status_code == 404:
                raise GitHubAPIError(
                    f"没有找到仓库：{owner}/{repository}"
                )

            response.raise_for_status()
            return response.json()

        except requests.Timeout as error:
            raise GitHubAPIError("请求超时，请检查网络。") from error

        except requests.ConnectionError as error:
            raise GitHubAPIError("无法连接 GitHub。") from error

        except requests.HTTPError as error:
            raise GitHubAPIError(
                f"GitHub 返回 HTTP 错误：{error}"
            ) from error

        except requests.RequestException as error:
            raise GitHubAPIError(
                f"请求失败：{error}"
            ) from error

    def get_latest_commits(
        self,
        owner: str,
        repository: str,
        limit: int = 3,
    ) -> list[dict[str, Any]]:
        """获取仓库最近的 Commit。"""
        url = f"{self.BASE_URL}/repos/{owner}/{repository}/commits"

        try:
            response = self.session.get(
                url,
                params={"per_page": limit},
                timeout=self.timeout,
            )

            if response.status_code == 404:
                raise GitHubAPIError(
                    f"没有找到仓库：{owner}/{repository}"
                )

            response.raise_for_status()
            return response.json()

        except requests.Timeout as error:
            raise GitHubAPIError("请求超时，请检查网络。") from error

        except requests.ConnectionError as error:
            raise GitHubAPIError("无法连接 GitHub。") from error

        except requests.HTTPError as error:
            raise GitHubAPIError(
                f"GitHub 返回 HTTP 错误：{error}"
            ) from error

        except requests.RequestException as error:
            raise GitHubAPIError(
                f"请求失败：{error}"
            ) from error
