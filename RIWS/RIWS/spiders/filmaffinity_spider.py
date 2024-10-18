import scrapy
from RIWS.items import FAFilmItem

class FilmaffinitySpider(scrapy.Spider):
    name = "fa_spider"
    base_url = 'https://www.filmaffinity.com/es/category.php?id=2024films'
    start_urls = [
        base_url
    ]

    def parse(self, response):
        # Loop over each film in the list
        for film in response.css('div.movie-poster'):
            item = FAFilmItem()
            item['title'] = film.css('div.movie-title a::text').get()
            film_url = film.css('div.movie-title a::attr(href)').get()
            item['url'] = response.urljoin(film_url)  # Create absolute URL
            # Pass the item to the next request and call the parse_film method
            yield response.follow(film_url, callback=self.parse_film, meta={'item': item})

    def parse_film(self, response):
        # Extract the previously passed item
        item = response.meta['item']
        
        # Extract the synopsis from the film's page
        item['synopsis'] = response.css('dd[itemprop="description"]::text').get()
        
        # Return the complete item
        yield item
