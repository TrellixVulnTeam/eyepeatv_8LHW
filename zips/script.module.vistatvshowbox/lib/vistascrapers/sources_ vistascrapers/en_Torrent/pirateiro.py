# -*- coding: utf-8 -*-

#  ..#######.########.#######.##....#..######..######.########....###...########.#######.########..######.
#  .##.....#.##.....#.##......###...#.##....#.##....#.##.....#...##.##..##.....#.##......##.....#.##....##
#  .##.....#.##.....#.##......####..#.##......##......##.....#..##...##.##.....#.##......##.....#.##......
#  .##.....#.########.######..##.##.#..######.##......########.##.....#.########.######..########..######.
#  .##.....#.##.......##......##..###.......#.##......##...##..########.##.......##......##...##........##
#  .##.....#.##.......##......##...##.##....#.##....#.##....##.##.....#.##.......##......##....##.##....##
#  ..#######.##.......#######.##....#..######..######.##.....#.##.....#.##.......#######.##.....#..######.

'''
    OpenScrapers Project
    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''

import re
import urllib
import urlparse

from vistascrapers.modules import cfscrape
from vistascrapers.modules import cleantitle
from vistascrapers.modules import debrid
from vistascrapers.modules import source_utils


class source:
	def __init__(self):
		self.priority = 1
		self.language = ['en']
		self.domains = ['pirateiro.unblockit.biz']
		self.base_link = 'https://pirateiro.unblockit.id'
		self.search_link = '/torrents/?search=%s'
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
			if url is None:
				return
			url = urlparse.parse_qs(url)
			url = dict([(i, url[i][0]) if url[i] else (i, '') for i in url])
			url['title'], url['premiered'], url['season'], url['episode'] = title, premiered, season, episode
			url = urllib.urlencode(url)
			return url
		except:
			return


	def sources(self, url, hostDict, hostprDict):
		sources = []
		try:
			if url is None:
				return sources

			if debrid.status() is False:
				return sources

			data = urlparse.parse_qs(url)
			data = dict([(i, data[i][0]) if data[i] else (i, '') for i in data])

			title = data['tvshowtitle'] if 'tvshowtitle' in data else data['title']
			title = title.replace('&', 'and').replace('Special Victims Unit', 'SVU')

			hdlr = 'S%02dE%02d' % (int(data['season']), int(data['episode'])) if 'tvshowtitle' in data else data['year']

			query = '%s %s' % (title, hdlr)
			query = re.sub('(\\\|/| -|:|;|\*|\?|"|\'|<|>|\|)', '', query)

			url = self.search_link % urllib.quote_plus(query)
			url = urlparse.urljoin(self.base_link, url)
			# log_utils.log('url = %s' % url, log_utils.LOGDEBUG)

			try:
				r = self.scraper.get(url).content
				links = zip(re.findall('href="(magnet:.+?)"', r, re.DOTALL), re.findall('((?:\d+\,\d+\.\d+|\d+\.\d+|\d+\,\d+|\d+)\s*(?:GiB|MiB|GB|MB))', r, re.DOTALL))

				for link in links:
					url = link[0].split('&xl')[0]

					size = link[1]

					name = url.split('&dn=')[1]
					name = urllib.unquote_plus(name).replace(' ', '.')
					if source_utils.remove_lang(name):
						continue

					t = name.split(hdlr)[0].replace(data['year'], '').replace('(', '').replace(')', '').replace('&', 'and').replace('.US.', '.').replace('.us.', '.')
					if cleantitle.get(t) != cleantitle.get(title):
						continue

					if hdlr not in name:
						continue

					quality, info = source_utils.get_release_quality(name, url)

					try:
						div = 1 if size.endswith('GB') else 1024
						size = float(re.sub('[^0-9|/.|/,]', '', size.replace(',', '.'))) / div
						size = '%.2f GB' % size
						info.insert(0, size)
					except:
						pass

					info = ' | '.join(info)

					sources.append({'source': 'torrent', 'quality': quality, 'language': 'en', 'url': url,
											'info': info, 'direct': False, 'debridonly': True})

				return sources

			except:
				source_utils.scraper_error('PIRATEIRO')
				return sources

		except:
			source_utils.scraper_error('PIRATEIRO')
			return sources


	def resolve(self, url):
		return url