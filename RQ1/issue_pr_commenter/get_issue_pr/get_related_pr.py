# Async client for github.com/12f23eddde/github-scraper
# ref: https://blog.jonlu.ca/posts/async-python-http

import os
import asyncio
import aiohttp
import logging
from tqdm.asyncio import tqdm
from typing import Callable, Any, Dict, List, Tuple
import csv


class GithubScraperClient:
    def __init__(
        #self, baseurl: str, auth: str, num_workers=10, num_retries=3, max_pages=10
        self, baseurl: str, auth: str, num_workers=7, num_retries=3, max_pages=10
    ) -> None:
        """
        Initialize a GithubScraperClient.
        :param baseurl: the base url of the scraper
        :param auth: the authorization token
        :param num_workers: the number of workers to fetch pages (default: 10, <=30 is recommended)
        :param num_retries: the number of retries to fetch pages (default: 3)
        :param max_pages: limit number of subrequests on a single fetch (default: 10, <=10 is recommended)
        """
        self._logger = logging.getLogger(__name__)
        self._baseurl = baseurl
        self._auth = auth
        self._num_retries = num_retries
        self._max_pages = max_pages
        self._semaphore = asyncio.Semaphore(num_workers)

    async def _fetch(self, url: str, params: Dict[str, str]) -> Dict[str, Any]:
        """
        Fetch a URL and return the response.
        """
        headers = {
            "Authorization": self._auth,
        }
        async with self._semaphore:
            async with self._session.get(
                url, params=params, headers=headers
            ) as response:
                data = await response.json()
                if response.status != 200:
                    raise Exception(
                        f"{response.status} {response.reason} {data['error']}"
                    )
                return data

    async def _get(self, url: str, params: Dict[str, str]) -> List[Dict[str, Any]]:
        """
        fetch a url with pagination and error handling and return the response.
        """
        has_next = True
        all_res = []
        retries = self._num_retries

        while has_next and retries > 0:
            data = None
            try:
                data = await self._fetch(url, params)
            except Exception as e:
                self._logger.error(
                    f"{e}: retrying {self._num_retries-retries+1}/{self._num_retries}"
                )
                # not found, skip this page
                if "not found" in str(e).lower():
                    retries = 0
                else:
                    retries -= 1
                    await asyncio.sleep(10)
                continue

            if len(data) == 0 or "data" not in data.keys():
                raise Exception(f"{params} has no body")

            all_res.extend(data["data"])

            # update params for next iter
            has_next = "next" in data.keys()
            if has_next:
                retries = self._num_retries
                params["fromPage"] = int(data["current"]) + 1

        # failed, return current list
        if retries == 0:
            self._logger.error(
                f"fetch {url} {params} failed after {self._num_retries} retries"
            )

        return all_res

    async def _get_with_callback(
        self, url: str, params: Dict[str, str], callback: Callable[[List, Dict], Any]
    ) -> None:
        """
        get a url and execute a callback on each page.
        """
        all_res = await self._get(url, params)
        callback(all_res, params)

    def get_all(
        self, url: str, queries: List[Dict[str, str]]
    ) -> List[List[Dict[str, Any]]]:
        """
        fetch all pages of a url and return the response.
        :param url: the url to fetch
        :param queries: the list of params
        :return: a list of all responses
        """
        conn = aiohttp.TCPConnector(limit_per_host=100, limit=0, ttl_dns_cache=300)
        loop = asyncio.get_event_loop()

        async def async_worker():
            self._session = aiohttp.ClientSession(connector=conn)
            try:
                res = await tqdm.gather(*(self._get(url, params) for params in queries))
                return res
            except Exception as e:
                self._logger.exception(e)
            finally:
                await self._session.close()

        res = loop.run_until_complete(async_worker())
        conn.close()
        return res

    def get_all_with_callback(
        self,
        url: str,
        queries: List[Dict[str, str]],
        callback: Callable[[List, Dict], Any],
    ) -> None:
        """
        fetch all pages of a url and execute a callback on each page.
        :param url: the url to fetch
        :param queries: the list of params
        :param callback: the callback to execute on each page (result: list, params: dict) -> None
        """
        # Initialize connection pool
        conn = aiohttp.TCPConnector(limit_per_host=100, limit=0, ttl_dns_cache=300)
        loop = asyncio.get_event_loop()

        async def async_worker():
            self._session = aiohttp.ClientSession(connector=conn)
            try:
                await tqdm.gather(
                    *(
                        self._get_with_callback(url, params, callback)
                        for params in queries
                    )
                )
            except Exception as e:
                self._logger.exception(e)
            finally:
                await self._session.close()

        loop.run_until_complete(async_worker())
        conn.close()


    def get_issues_with_callback(
        self, issues_list: List[Tuple[str, int]], callback: Callable[[List, Dict], Any]
    ) -> None:
        """
        fetch a repo's issue and execute a callback on it.
        :param issues_list: the list of issues [(repo, number)]
        :param number: the issue number to fetch
        :param callback: the callback to execute on the issue (results: list, params: dict) -> None
        """
        url = f"{self._baseurl}/issue"
        queries = [
            {
                "owner": name_with_owner.split("/")[0],
                "name": name_with_owner.split("/")[1],
                "id": number,
            }
            for name_with_owner, number in issues_list
        ]

        self.get_all_with_callback(url, queries, callback)



if __name__ == "__main__":
    # create a github scraper
    scraper = GithubScraperClient(
        baseurl="https://scraper.12f23eddde.workers.dev/github", auth="OSSLab@PKU"
    )

    file1 = open('url2.csv', 'r')
    csv_reader = csv.reader(file1)
    next(csv_reader)

    file2 = open('issue_pr.csv', 'w')
    csv_writer = csv.writer(file2)
    csv_writer.writerow(['issue_id','issue_url','pr_url'])

    queries = []

    # do not iterate over the whole list and make a single request, which makes the request synchronous
    for row in csv_reader:
        try:
            url_items = row[2].split('/')

            name_with_owner = url_items[3]+'/'+url_items[4]
            pr_number = int(url_items[6])
            issue_number = int(row[1].split('/')[6])
            queries.append({
                "owner": url_items[3],
                "name": url_items[4],
                "id": pr_number,
                "issue_id": row[0],
                "issue_url": row[1],
                "issue_number": issue_number
            })
        except:
            continue
    
    print(f"{len(queries)} queries", queries[:10])

    # callback save the results (in this case, the body of the PR)
    def callback(results: list, params: dict) -> None:
        # read params
        owner = params['owner']
        name = params['name']
        issue_id = params['issue_id']
        number = params['id']
        issue_url = params['issue_url']
        issue_number = params['issue_number']
        pr_url = f"https://github.com/{owner}/{name}/pull/{number}"

        #print(issue_url, issue_number, '+++++++++++++++++++')

        flag = False
        if len(results) == 0:
            return
        for res in results:
            #print(res)
            if res['itemId'] == '1':
                if 'mentionedLinks' in res.keys() and len(res['mentionedLinks']) != 0:
                    if issue_url in res['mentionedLinks']:
                        flag = True
            elif res['itemId'] == 'global' and ('title' in res.keys() and res['title'].find(str(issue_number)) > 0):
                lag = True
        if flag:
            csv_writer.writerow([issue_id, issue_url, pr_url])
            
    # fetch the PR bodies
    scraper.get_all_with_callback(f"{scraper._baseurl}/pull", queries, callback)

    file1.close()
    file2.close()