import scrapy


class Sozler2Spider(scrapy.Spider):
    name = 'sozler2'
    allowed_domains = ['sarkisozlerihd.com']
    start_urls = ['http://www.sarkisozlerihd.com/sarkicilar/']

    # custom_settings = {'FEED_EXPORT_ENCODING': 'ISO-8859-1'}

    def parse(self, response):

    	artist_info = response.xpath('//*[@class = "full-screen-list-inside clearfix"]/ul//li')

    	for artist in artist_info:

    		artist_page = artist.xpath('.//*[@class = "otto"]/a/@href').extract_first()
    		artist_name = artist.xpath('.//*[@class = "otto"]/a/text()').extract_first()

    		yield scrapy.Request(artist_page,
    							 callback = self.parse_songs,
    							 meta = {'Artist Name':artist_name, 'Artist Page':artist_page})


    	next_page_list = response.xpath('.//*[@class = "row margint10"]//*[@class="clearfix"]/li')

    	for i in next_page_list:
    		if i.xpath('./a/text()').extract_first() == 'İleri':
    			next_page = i.xpath('./a/@href').extract_first()
    		else:
    			next_page = None

    	yield scrapy.Request(next_page)

    def parse_songs(self, response):
    	artist_page = response.meta['Artist Page']
    	artist_name = response.meta['Artist Name']

    	song_names = response.xpath('//*[@class = "list-line margint10 clearfix"]/a/text()').extract()
    	song_links = response.xpath('//*[@class = "list-line margint10 clearfix"]/a/@href').extract()

    	for song_name, song_link in zip(song_names, song_links):
    		response.meta['Song Name'] = song_name
    		response.meta['Song Link'] = song_link

    		yield scrapy.Request(song_link, callback = self.parse_lyrics, meta = {'Artist Name':artist_name, 'Artist Page':artist_page,'Song Name':song_name,'Song Link':song_link})

    def parse_lyrics(self, response):
    	artist_name = response.meta['Artist Name']
    	artist_page = response.meta['Artist Page']
    	song_name = response.meta['Song Name']
    	song_link = response.meta['Song Link']

    	lyrics = response.xpath('//*[@class="lyric-text margint20 marginb20"]/p/text()').extract()
    	lyrics = '\n'.join(lyrics)

    	yield {'Artist Name':artist_name, 'Artist Page':artist_page,'Song Name':song_name,'Song Link':song_link, 'Lyrics':lyrics}

    	# if detect(lyrics) == 'tr':
    	# 	yield {'Artist Name':artist_name, 'Artist Page':artist_page,'Song Name':song_name,'Song Link':song_link, 'Lyrics':lyrics}
    	# else:
    	# 	pass


