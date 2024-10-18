import scrapy
from RIWS.items import FAFilmItem

class FilmaffinitySpider(scrapy.Spider):
    name = "fa_spider"
    start_page = 1
    base_url = 'https://www.filmaffinity.com/es/category.php?id=2024films&page={}'.format(start_page)
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

        current_page = int(response.url.split('page=')[-1].split('&')[0])
        max_pages = 2

        if current_page < max_pages:
            next_page = current_page + 1
            next_page_url = f'https://www.filmaffinity.com/es/category.php?id=2024films&page={next_page}'
            # Realizar la solicitud de la siguiente página
            yield scrapy.Request(next_page_url, callback=self.parse)

    def parse_film(self, response):
        # Extract the previously passed item
        item = response.meta['item']
        
        # Extract the synopsis from the film's page
        item['synopsis'] = response.css('dd[itemprop="description"]::text').get()
        
        # Return the complete item
        yield item
