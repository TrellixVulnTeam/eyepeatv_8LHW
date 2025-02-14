# -*- coding: UTF-8 -*-

#  ..#######.########.#######.##....#..######..######.########....###...########.#######.########..######.
#  .##.....#.##.....#.##......###...#.##....#.##....#.##.....#...##.##..##.....#.##......##.....#.##....##
#  .##.....#.##.....#.##......####..#.##......##......##.....#..##...##.##.....#.##......##.....#.##......
#  .##.....#.########.######..##.##.#..######.##......########.##.....#.########.######..########..######.
#  .##.....#.##.......##......##..###.......#.##......##...##..########.##.......##......##...##........##
#  .##.....#.##.......##......##...##.##....#.##....#.##....##.##.....#.##.......##......##....##.##....##
#  ..#######.##.......#######.##....#..######..######.##.....#.##.....#.##.......#######.##.....#..######.

import base64
import json
import re
import urllib
import urlparse

from openscrapers.modules import cfscrape
from openscrapers.modules import cleantitle
from openscrapers.modules import debrid
from openscrapers.modules import source_utils


class source:
    def __init__(self):
        self.priority = 1
        self.language = ['en']
        self.domains = ['directdownload.tv']
        self.base_link = 'https://directdownload.tv'
        # self.search_link = 'L2FwaT9rZXk9NEIwQkI4NjJGMjRDOEEyOSZxdWFsaXR5W109SERUViZxdWFsaXR5W109RFZEUklQJnF1YWxpdHlbXT03MjBQJnF1YWxpdHlbXT1XRUJETCZxdWFsaXR5W109V0VCREwxMDgwUCZxdWFsaXR5W109MTA4MFAtWDI2NSZsaW1pdD0yMCZrZXl3b3JkPQ=='
        self.search_link = base64.b64decode('L2FwaT9rZXk9NEIwQkI4NjJGMjRDOEEyOSZrZXl3b3JkPQ==')
        self.b_link = 'aHR0cDovL2lwdjYuaWNlZmlsbXMuaW5mbw=='
        self.u_link = 'aHR0cDovL2lwdjYuaWNlZmlsbXMuaW5mby9tZW1iZXJzb25seS9jb21wb25lbnRzL2NvbV9pY2VwbGF5ZXIvdmlkZW8ucGhwP2g9Mzc0Jnc9NjMxJnZpZD0lcyZpbWc9'
        self.r_link = 'aHR0cDovL2lwdjYuaWNlZmlsbXMuaW5mby9pcC5waHA/dj0lcyY='
        self.j_link = 'aHR0cDovL2lwdjYuaWNlZmlsbXMuaW5mby9tZW1iZXJzb25seS9jb21wb25lbnRzL2NvbV9pY2VwbGF5ZXIvdmlkZW8ucGhwQWpheFJlc3AucGhwP3M9JXMmdD0lcw=='
        self.p_link = 'aWQ9JXMmcz0lcyZpcXM9JnVybD0mbT0lcyZjYXA9KyZzZWM9JXMmdD0lcw=='
        self.scraper = cfscrape.create_scraper()

    def movie(self, imdb, title, localtitle, aliases, year):
        try:
            url = {'imdb': imdb, 'title': title, 'year': year}
            url = urllib.urlencode(url)
            return url
        except:
            return

    def tvshow(self, imdb, tvdb, tvshowtitle, localtvshowtitle, aliases, year):
        try:
            url = {'imdb': imdb, 'tvdb': tvdb, 'tvshowtitle': tvshowtitle, 'year': year}
            url = urllib.urlencode(url)
            return url
        except:
            return

    def episode(self, url, imdb, tvdb, title, premiered, season, episode):
        try:
            if url == None: return
            url = urlparse.parse_qs(url)
            url = dict([(i, url[i][0]) if url[i] else (i, '') for i in url])
            url['title'], url['premiered'], url['season'], url['episode'] = title, premiered, season, episode
            url = urllib.urlencode(url)
            return url
        except:
            return

    def directdl_cache(self, url):
        try:
            url = urlparse.urljoin(base64.b64decode(self.b_link), url)
            result = self.scraper.get(url).content
            result = re.compile('id=(\d+)>.+?href=(.+?)>').findall(result)
            result = [(re.sub('http.+?//.+?/', '/', i[1]), 'tt' + i[0]) for i in result]
            return result
        except:
            return

    def sources(self, url, hostDict, hostprDict):
        try:
            sources = []
            hostDict = hostprDict + hostDict
            if url is None:
                return sources
            if debrid.status() is False:
                raise Exception()
            data = urlparse.parse_qs(url)
            data = dict([(i, data[i][0]) if data[i] else (i, '') for i in data])
            try:
                links = []
                f = ['S%02dE%02d' % (int(data['season']), int(data['episode']))]
                t = re.sub('(\\\|/| -|:|;|\*|\?|"|\'|<|>|\|)', '', data['tvshowtitle'])
                t = t.replace("&", "")
                q = self.search_link + urllib.quote_plus('%s %s' % (t, f[0]))
                q = urlparse.urljoin(self.base_link, q)
                result = self.scraper.get(q).content
                result = json.loads(result)
                result = result['results']
            except:
                links = result = []
            for i in result:
                try:
                    if not cleantitle.get(t) == cleantitle.get(i['showName']):
                        raise Exception()
                    y = i['release']
                    y = re.compile('[\.|\(|\[|\s](\d{4}|S\d*E\d*)[\.|\)|\]|\s]').findall(y)[-1]
                    y = y.upper()
                    if not any(x == y for x in f):
                        raise Exception()
                    quality = i['quality']
                    quality, info = source_utils.get_release_quality(quality)

                    try:
                        size = i['size']
                        size = float(size) / 1024
                        size = '%.2f GB' % size
                        info.append(size)
                    except:
                        pass

                    info = ' | '.join(info)
                    url = i['links']
                    # for x in url.keys(): links.append({'url': url[x], 'quality': quality, 'info': info})
                    links = []
                    for x in url.keys():
                        links.append({'url': url[x], 'quality': quality})
                    for link in links:
                        try:
                            url = link['url']
                            quality2 = link['quality']
                            if len(url) > 1:
                                raise Exception()
                            url = url[0].encode('utf-8')
                            host = re.findall('([\w]+[.][\w]+)$', urlparse.urlparse(url.strip().lower()).netloc)[0]
                            if host not in hostDict:
                                raise Exception()
                            host = host.encode('utf-8')
                            sources.append(
                                {'source': host, 'quality': quality2, 'language': 'en', 'url': url, 'info': info,
                                 'direct': False, 'debridonly': True})
                        except:
                            pass
                except:
                    pass
            return sources
        except:
            return sources

    def resolve(self, url):
        try:
            b = urlparse.urlparse(url).netloc
            b = re.compile('([\w]+[.][\w]+)$').findall(b)[0]
            if not b in base64.b64decode(self.b_link): return url
            u, p, h = url.split('|')
            r = urlparse.parse_qs(h)['Referer'][0]
            c = self.scraper.get(r)
            result = self.scraper.post(u, data=p, headers={'referer': r}, cookies=c.cookies)
            url = result.split('url=')
            url = [urllib.unquote_plus(i.strip()) for i in url]
            url = [i for i in url if i.startswith('http')]
            url = url[-1]
            return url
        except:
            return
