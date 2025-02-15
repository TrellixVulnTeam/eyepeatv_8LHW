# -*- coding: UTF-8 -*-

#  ..#######.########.#######.##....#..######..######.########....###...########.#######.########..######.
#  .##.....#.##.....#.##......###...#.##....#.##....#.##.....#...##.##..##.....#.##......##.....#.##....##
#  .##.....#.##.....#.##......####..#.##......##......##.....#..##...##.##.....#.##......##.....#.##......
#  .##.....#.########.######..##.##.#..######.##......########.##.....#.########.######..########..######.
#  .##.....#.##.......##......##..###.......#.##......##...##..########.##.......##......##...##........##
#  .##.....#.##.......##......##...##.##....#.##....#.##....##.##.....#.##.......##......##....##.##....##
#  ..#######.##.......#######.##....#..######..######.##.....#.##.....#.##.......#######.##.....#..######.

'''
    bnwmovies scraper for Exodus forks.
    Nov 9 2018 - Checked

    Updated and refactored by someone.
    Originally created by others.
'''
import re
import traceback

from vistascrapers.modules import cfscrape
from vistascrapers.modules import cleantitle
from vistascrapers.modules import log_utils


class source:
    def __init__(self):
        self.priority = 1
        self.language = ['en']
        self.domains = ['www.bnwmovies.com']
        self.base_link = 'http://www.bnwmovies.com/'
        self.search_link = '%s/search?q=bnwmovies.com+%s+%s'
        self.scraper = cfscrape.create_scraper(0)

    def movie(self, imdb, title, localtitle, aliases, year):
        try:
            scrape = title.lower().replace(' ', '+').replace(':', '')

            start_url = self.search_link % (self.base_link, scrape, year)
            html = self.scraper.get(start_url).content
            results = re.compile('href="(.+?)"', re.DOTALL).findall(html)
            for url in results:
                if self.base_link in url:
                    if 'webcache' in url:
                        continue
                    if cleantitle.get(title) in cleantitle.get(url):
                        chkhtml = self.scraper.get(url).content
                        chktitle = re.compile('<title.+?>(.+?)</title>', re.DOTALL).findall(chkhtml)[0]
                        if cleantitle.get(title) in cleantitle.get(chktitle):
                            if year in chktitle:
                                return url
            return
        except:
            failure = traceback.format_exc()
            log_utils.log('BNWMovies - Exception: \n' + str(failure))
            return

    def sources(self, url, hostDict, hostprDict):
        try:
            sources = []
            if url == None: return sources

            html = self.scraper.get(url).content

            Links = re.compile('<source.+?src="(.+?)"', re.DOTALL).findall(html)
            for link in Links:
                sources.append({'source': 'BNW', 'quality': 'SD', 'language': 'en', 'url': link, 'direct': True,
                                'debridonly': False})
            return sources
        except:
            failure = traceback.format_exc()
            log_utils.log('BNWMovies - Exception: \n' + str(failure))
            return sources

    def resolve(self, url):
        return url
