import requests
import bs4

import typing
import pathlib


class Libgen:
    def __init__(
        self,
        site: str = "libgen.is",
        verbose: bool = False,
        headers: dict = {"User-Agent": "Not A Bot"},
    ):
        self.site = site
        self.url = f"https://{self.site}"
        self.headers = headers

    def get_book(self, book: str, page: int = 1) -> dict:
        search = f'{self.url}/search.php?&req={"+".join(book.split(" "))}&page={page}'
        results = requests.get(search, headers=self.headers)
        soup = bs4.BeautifulSoup(results.content, "html5lib")
        d = {}
        for _index_1, _content_1 in enumerate(soup.find_all("tr")):
            if _index_1 not in [0, 1, 2, len(soup.find_all("tr")) - 1]:
                id = ""
                for _index_2, _content_2 in enumerate(_content_1.find_all("td")):
                    if _index_2 == 0:
                        d[_content_2.text] = {}
                        d[_content_2.text]["authors"] = []
                        id = _content_2.text
                    links = _content_2.find_all("a")
                    for _content_3 in links:
                        if "column=author" in _content_3.get("href"):
                            d[id]["authors"].append(_content_3.text)
                        elif "column[]=author" in _content_3.get("href"):
                            d[id]["authors"].append(_content_3.text)
                        elif _content_3.get("href").startswith("book/index.php"):
                            try:
                                title = _content_3.text.replace(
                                    _content_3.find("i").text, ""
                                )
                            except AttributeError:
                                title = _content_3.text
                            d[id]["title"] = title
                            d[id]["link"] = _content_3.get("href").split("md5=")[1]
        return d

    def get_download_links(self, link):
        content = requests.get(f"http://library.lol/main/{link}", headers=self.headers)
        soup = bs4.BeautifulSoup(content.content, "html5lib")
        _links = soup.find("ul").find_all("a")
        links = []
        for i in _links:
            links.append(i.get("href"))
        return links

    def download_book(self, link: str, path: typing.Union[str, pathlib.Path]):
        content = requests.get(link, headers=self.headers).content
        with open(path, "wb") as f:
            f.write(content)