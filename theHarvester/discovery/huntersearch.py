from theHarvester.discovery.constants import *
from theHarvester.lib.core import *
from theHarvester.parsers import myparser


class SearchHunter:

    def __init__(self, word, limit, start):
        self.word = word
        self.limit = limit
        self.start = start
        self.key = Core.hunter_key()
        if self.key is None:
            raise MissingKey(True)
        self.total_results = ""
        self.counter = start
        self.database = f'https://api.hunter.io/v2/domain-search?domain={word}&api_key={self.key}&limit={self.limit}'

    async def do_search(self):
        responses = await AsyncFetcher.fetch_all([self.database], headers={'User-Agent': Core.get_user_agent()})
        self.total_results += responses[0]

    async def process(self):
        await self.do_search()  # Only need to do it once.

    async def get_emails(self):
        rawres = myparser.Parser(self.total_results, self.word)
        return rawres.emails()

    async def get_hostnames(self):
        rawres = myparser.Parser(self.total_results, self.word)
        return rawres.hostnames()

    async def get_profiles(self):
        rawres = myparser.Parser(self.total_results, self.word)
        return rawres.profiles()
