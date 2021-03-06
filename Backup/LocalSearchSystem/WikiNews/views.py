from django.shortcuts import render
import scrapy
import re
import pandas as pd
import unicodedata
from scrapy.crawler import CrawlerProcess
from urllib.parse import urlparse
from twisted.internet import reactor, defer
from scrapy.crawler import CrawlerRunner
from scrapy.utils.log import configure_logging
from .models import WikiNewsItem

# Create your views here.

result = []
all_urls = []
Paragraph_Data = []
continents = []
continents_urls = []


class Wikipedia(scrapy.Spider):
    name = "Wikipedia"
    # start_urls = [
    #     "https://en.wikinews.org/wiki/Main_Page"
    # ]

    def parse(self, response):
        for sel in response.xpath('//center//big//b'):
            title = sel.xpath('a/text()').extract()
            link = sel.xpath('a/@href').extract()
            continents.append(zip(title, link))


class Wikinews(scrapy.Spider):
    name = "Wikinews"

    def parse(self, response):
        for sel in response.xpath('//ul/li'):
            title = sel.xpath('a/text()').extract()
            link = sel.xpath('a/@href').extract()
            result.append((title[0], link[0]))


class Wikinews_items(scrapy.Spider):
    name = "Wikinews_items"
    allowed_domains = ['en.wikinews.org']

    def parse(self, response):
        parsed_uri = urlparse(response.url)
        domain = '{uri.scheme}://{uri.netloc}/'.format(uri=parsed_uri)

        def _clean(value):
            value = ' '.join(value)
            value = value.replace('\n', '')
            value = unicodedata.normalize("NFKD", value)
            value = re.sub(r' , ', ', ', value)
            value = re.sub(r' \( ', ' (', value)
            value = re.sub(r' \) ', ') ', value)
            value = re.sub(r' \)', ') ', value)
            value = re.sub(r'\[\d.*\]', ' ', value)
            value = re.sub(r' +', ' ', value)
            return value.strip()

        strings = ""
        for i in range(0, 100):
            try:
                for node in response.xpath('//*[@id="mw-content-text"]/div/p[{}]'.format(i)):
                    text = _clean(node.xpath('string()').extract())
                    if len(text):
                        strings = strings + text + "<br>"
            except Exception as error:
                pass

        try:
            image = 'https:' + response.xpath('//img[@class="thumbimage"]/@src').extract_first()
        except:
            image = ""

        paragraph_data = {
            'title': response.css('#firstHeading::text').extract_first(),
            'lastUpdated': response.xpath('//*[@id="publishDate"]/@title').extract_first(),
            'image': image,
            'text': strings
        }
        Paragraph_Data.append(paragraph_data)


configure_logging()
runner = CrawlerRunner()


@defer.inlineCallbacks
def crawl(url):
    yield runner.crawl(Wikipedia,start_urls=[url])
    for title, link in continents[0]:
        con_cat = 'https://en.wikinews.org/wiki/Category:' + link.replace('/wiki/', '')
        continents_urls.append(con_cat)

    yield runner.crawl(Wikinews, start_urls=continents_urls)
    df = pd.DataFrame(data=result, columns=["title", "link"])
    df.link = 'https://en.wikinews.org' + df.link
    all_urls = list(df.link)

    yield runner.crawl(Wikinews_items, start_urls=all_urls)
    reactor.stop()


def ScrapWikiNews(request):
    if request.method == 'POST':
        url = request.POST.get('urlinput')
        crawl(url)
        reactor.run()
        wikinewsdata = pd.DataFrame(Paragraph_Data)

        # wikinewsdata['image'] = wikinewsdata['image'].apply(lambda x: ('https:' + x) if x != None else x)
        # print(wikinewsdata)
        items = WikiNewsItem.objects.all()
        titles=[]
        for item in items:
            titles.append(item.title)
        wikinewsdata=wikinewsdata[wikinewsdata["title"].isin(titles) == False]
        print(wikinewsdata)
        try:
            WikiNewsItem.objects.bulk_create(WikiNewsItem(**vals) for vals in wikinewsdata.to_dict('records'))
        except:
            pass

    return  render(request,'web-scrapping.html')



def ItemManagementView(request):
    itemList = WikiNewsItem.objects.all()
    return render(request, 'item-management.html', {'itemList': itemList})

def WebScrappingView(request):
    return render(request, 'web-scrapping.html')

def ItemDetailView(request, itemId):
    print(itemId)
    items = WikiNewsItem.objects.filter(id=itemId)
    paragraphs =[]
    for field in items:
        content = field.text
        print(content)
        paragraphs = content.split('<br>')

    return render(request, 'details.html', {'items':items,'paragraphs':paragraphs})


def SearchView(request):
    return render(request, 'search.html')

def SearchResultView(request):
    return render(request,'search-result.html')

def SearchItemResultView(request):
    return render(request, 'search-item-result.html')



def DelItem(request,itemId):
    # if request.session.get('username')==None:
    #     return HttpResponseRedirect('/users/login')
    print(itemId)
    item=WikiNewsItem.objects.get(id=itemId)
    item.delete()
    return ItemManagementView(request)