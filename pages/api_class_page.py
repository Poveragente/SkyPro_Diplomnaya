import requests
import allure
import json
from typing import Any, Dict, Optional, List


class ApiPage:
    def __init__(self, base_url: str, headers: Dict[str, str], api_version: str = "v1.5"):
        self.base_url = base_url.rstrip("/")
        self.headers = headers
        self.api_version = api_version

    def _request(
        self,
        method: str,
        endpoint: str,
        params: Optional[Dict] = None,
        data: Optional[Any] = None,
    ) -> requests.Response:
        url = f"{self.base_url}/{self.api_version}/{endpoint}"
        allure.attach(
            name="API Request",
            body=f"{method} {url}\nParams: {params}",
            attachment_type=allure.attachment_type.TEXT,
        )
        try:
            resp = requests.request(
                method, url, headers=self.headers,
                params=params, json=data, timeout=15,
            )
        except requests.exceptions.RequestException as e:
            allure.attach(str(e), name="Request Exception",
                          attachment_type=allure.attachment_type.TEXT)
            raise

        try:
            body = resp.json()
        except ValueError:
            body = resp.text

        allure.attach(
            name=f"API Response ({resp.status_code})",
            body=(json.dumps(body, ensure_ascii=False, indent=2)
                  if isinstance(body, (dict, list)) else str(body)),
            attachment_type=(allure.attachment_type.JSON
                             if isinstance(body, (dict, list))
                             else allure.attachment_type.TEXT),
        )
        return resp

    # ── Фильмы ──────────────────────────────────────────

    def search_movies(self, query: str, limit: int = 10, page: int = 1) -> Dict[str, Any]:
        """Поиск фильмов по названию (v1.5)."""
        resp = self._request("GET", "movie/search",
                             params={"query": query, "limit": limit, "page": page})
        return resp.json()

    def get_movie_by_id(self, movie_id: int) -> Dict[str, Any]:
        """Получить фильм по ID."""
        resp = self._request("GET", f"movie/{movie_id}")
        return resp.json()

    def get_random_movie(self) -> Dict[str, Any]:
        """Получить рандомный фильм."""
        resp = self._request("GET", "movie/random")
        return resp.json()

    def get_movie_awards(
        self, movie_id: int, limit: int = 50,
    ) -> Dict[str, Any]:
        """Награды фильма по его ID (cursor-пагинация, v1.5)."""
        resp = self._request(
            "GET", "movie/awards",
            params={"movieId": movie_id, "limit": limit},
        )
        return resp.json()

    # ── Персоны ──────────────────────────────────────────

    def search_persons(self, query: str, limit: int = 10, page: int = 1) -> Dict[str, Any]:
        """Поиск персон по имени."""
        resp = self._request("GET", "person/search",
                             params={"query": query, "limit": limit, "page": page})
        return resp.json()

    def get_person_by_id(self, person_id: int) -> Dict[str, Any]:
        """Получить персону по ID."""
        resp = self._request("GET", f"person/{person_id}")
        return resp.json()

    def get_person_awards(
        self, person_id: int, limit: int = 50,
    ) -> Dict[str, Any]:
        """Награды персоны по её ID (cursor-пагинация, v1.5)."""
        resp = self._request(
            "GET", "person/awards",
            params={"personId": person_id, "limit": limit},
        )
        return resp.json()