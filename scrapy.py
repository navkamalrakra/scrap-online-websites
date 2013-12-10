
class MySpider(CrawlSpider):
    name = "Spidey"
    allowed_domains = ["example.com"]
    start_urls = ["http://www.example.com"]
    rules = (
        Rule(SgmlLinkExtractor(deny=('\.css', )), callback='parse_item'),
    )
    def parse_item(self, response):
        db = MySQLdb.connect("localhost","root","toor","db_name")
        cursor = db.cursor()
        hxs = HtmlXPathSelector(response)
        product_details_keys = ['name','brand','mrp','omrp','img']
        item_title = hxs.select('//h1[@id="product-heading"]/text()').extract()
        item_brand = hxs.select('//td/b/text()').extract()
        item_mrp = hxs.select('//table[@class="product-info"]/tr[@class="label"][last()-3]/td[last()]/text()').extract()
        item_our_price = hxs.select('//table[@class="product-info"]/tr[@class="label"][last()-2]/td[last()]/text()').extract()
        item_image = hxs.select('//div[@class="image-main"]/a/@href').extract()
        product_details = item_title + item_brand + item_mrp + item_our_price + item_image
        product_dict = dict(zip(product_details_keys,product_details))
        if 'name' in product_dict.keys():
                cursor.execute('INSERT into scrapped (name,brand,mrp,our_price,img_link) values (%s,%s,%s,%s,%s)', (product_dict['name'],product_dict['brand'],product_dict['mrp'],product_dict['omrp'],product_dict['img']))
            db.commit()
        db.close()
