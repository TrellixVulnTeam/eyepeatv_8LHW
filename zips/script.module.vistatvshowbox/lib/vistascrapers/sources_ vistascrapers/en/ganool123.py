# -*- coding: UTF-8 -*-
# -Cleaned and Checked on 03-16-2019 by JewBMX in Scrubs.

#  ..#######.########.#######.##....#..######..######.########....###...########.#######.########..######.
#  .##.....#.##.....#.##......###...#.##....#.##....#.##.....#...##.##..##.....#.##......##.....#.##....##
#  .##.....#.##.....#.##......####..#.##......##......##.....#..##...##.##.....#.##......##.....#.##......
#  .##.....#.########.######..##.##.#..######.##......########.##.....#.########.######..########..######.
#  .##.....#.##.......##......##..###.......#.##......##...##..########.##.......##......##...##........##
#  .##.....#.##.......##......##...##.##....#.##....#.##....##.##.....#.##.......##......##....##.##....##
#  ..#######.##.......#######.##....#..######..######.##.....#.##.....#.##.......#######.##.....#..######.

import re
import urllib
import urlparse

from vistascrapers.modules import cfscrape
from vistascrapers.modules import cleantitle
from vistascrapers.modules import source_utils


class source:
    def __init__(self):
        self.priority = 1
        self.language = ['en']
        self.domains = ['ganol.si', 'ganool123.com','idtube.ru'] # check for updated IP if needed idtube.ru
        self.base_link = 'http://79.124.60.188'
        self.search_link = '/search/?q=%s'
        self.scraper = cfscrape.create_scraper()

    def movie(self, imdb, title, localtitle, aliases, year):
        try:
            url = {'imdb': imdb, 'title': title, 'year': year}
            url = urllib.urlencode(url)
            return url
        except BaseException:
            return

    def sources(self, url, hostDict, hostprDict):
        sources = []
        try:
            if url is None:
                return sources
            data = urlparse.parse_qs(url)
            data = dict([(i, data[i][0]) if data[i] else (i, '') for i in data])
            q = '%s' % cleantitle.geturl(data['title'])
            url = self.base_link + self.search_link % q.replace('-', '+')
            r = self.scraper.get(url).content
            v = re.compile('<a href="(.+?)" class="ml-mask jt" title="(.+?)">\n<span class=".+?">(.+?)</span>').findall(
                r)
            for url, check, quality in v:
                t = '%s (%s)' % (data['title'], data['year'])
                if t not in check: raise Exception()
                r = self.scraper.get(url + '/watch.html').content
                url = re.compile('<iframe.+?src="(.+?)"').findall(r)[0]
                quality = source_utils.check_url(quality)
                valid, host = source_utils.is_host_valid(url, hostDict)
                if valid:
                    sources.append({'source': host, 'quality': quality, 'language': 'en', 'url': url, 'direct': False,
                                    'debridonly': False})
            return sources
        except BaseException:
            return sources

    def resolve(self, url):
        return url
