import scrapy
import time 
class AnimeSpider(scrapy.Spider):
    name = 'myanimelist'
    start_urls = ["https://myanimelist.net/topanime.php?limit=17000"]

    def parse(self,response):
        
        anime_urls = response.xpath("//tr[has-class('ranking-list')]/td[@class = 'title al va-t word-break']/a/@href")
        
       # for anime in anime_urls:
        #    url = anime.xpath("//tr[has-class('ranking-list')]/td[2]/a/@href").get()
        #    if url is not None:
        #        yield anime.follow(url , callback= self.parse_anime)
        yield from response.follow_all(anime_urls, self.parse_anime)
        next_page = response.xpath("//div/a[@class = 'link-blue-box next']/@href").get()
        if next_page != '?limit=17200':
            url = response.urljoin(next_page)
            yield scrapy.Request(url, callback=self.parse)


    def parse_anime(self,response):
        title = response.xpath("//div/h1/strong/text()").get()
        anime_type = response.xpath('//td[has-class("borderClass")]/div/div/span[contains(text(),"Type:")]/following-sibling::a/text()').get()
        episodes = response.xpath('//td[has-class("borderClass")]/div/div[span[contains(text(),"Episodes:")]]/text()')[1].get().strip()
        status = response.xpath('//td[has-class("borderClass")]/div/div[span[contains(text(),"Status:")]]/text()')[1].get().strip()
        aired = response.xpath('//td[has-class("borderClass")]/div/div[span[contains(text(),"Aired:")]]/text()')[1].get().strip()
        premiered = response.xpath('//td[has-class("borderClass")]/div/div/span[contains(text(),"Premiered:")]/following-sibling::a/text()').get()
        #broadcast = response.xpath('//td[has-class("borderClass")]/div/div[span[contains(text(),"Broadcast:")]]/text()').getall().strip()
        producers = response.xpath('//td[has-class("borderClass")]/div/div/span[contains(text(),"Producers:")]/following-sibling::a/text()').getall() 
        licensors = response.xpath('//td[has-class("borderClass")]/div/div/span[contains(text(),"Licensors:")]/following-sibling::a/text()').getall()    
        studios = response.xpath('//td[has-class("borderClass")]/div/div/span[contains(text(),"Studios:")]/following-sibling::a/text()').getall()
        source = response.xpath('//td[has-class("borderClass")]/div/div[span[contains(text(),"Source:")]]/text()')[1].get().strip()
        genres = response.xpath('//td[has-class("borderClass")]/div/div/span[contains(text(),"Genres:")]/following-sibling::a/text()').getall()
        duration = response.xpath('//td[has-class("borderClass")]/div/div[span[contains(text(),"Duration:")]]/text()')[1].get().strip()
        rating = response.xpath('//td[has-class("borderClass")]/div/div[span[contains(text(),"Rating:")]]/text()')[1].get().strip()
        score = response.xpath("//div/div[has-class('score-label')]/text()").get()
        rank = response.xpath("//div/div[has-class('di-ib ml12 pl20 pt8')]/span[1]/strong/text()").get()
        popularity = response.xpath("//div/div[has-class('di-ib ml12 pl20 pt8')]/span[2]/strong/text()").get()
        members = response.xpath("//div/div[has-class('di-ib ml12 pl20 pt8')]/span[3]/strong/text()").get()
        yield {'title':title, 
        'type': anime_type,
        'Episodes':episodes,
        'Status':status,
        'Aired':aired,
        'Premiered':premiered,
        #'Broadcast':broadcast,
        'Producers':producers,
        'Licensors':licensors,
        'Studios':studios,
        'Source':source,
        'Genres':genres,
        'Duration':duration,
        'Rating':rating,
        'Score':score,
        'Rank':rank,
        'Popularity':popularity,
        'Members':members}
        time.sleep(0)
