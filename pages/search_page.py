import requests


class MovieSearchPage:
    def __init__(self, base_url, headers):
        self.base_url = base_url
        self.headers = headers

    def search(self, query, limit=10, page=1):
        url = f"{self.base_url}/v1.4/movie/search"
        params = {"query": query, "limit": limit, "page": page}
        return requests.get(url, headers=self.headers, params=params)
