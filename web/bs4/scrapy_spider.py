# scrapy_spider.py
#pip install scrapy pandas
import scrapy
from scrapy.crawler import CrawlerProcess
from urllib.parse import urljoin
import pandas as pd
import re

class MySpider(scrapy.Spider):
    name = "my_spider"

    # Start URL
    start_urls = ['https://www.example.com']  # Replace with your target URL

    # Initialize data storage
    links = []
    resources = []
    texts = []

    def parse(self, response):
        # Extract all link URLs
        link_urls = response.css('a::attr(href)').getall()
        for href in link_urls:
            full_url = urljoin(response.url, href)
            self.links.append(full_url)

        # Extract all binary file URLs (images, .pdf, .docx)
        # Define patterns for binary files
        binary_patterns = re.compile(r'.*\.(jpg|jpeg|png|gif|bmp|tiff|pdf|docx|doc)$', re.IGNORECASE)
        resource_urls = []

        # Extract image URLs
        img_urls = response.css('img::attr(src)').getall()
        resource_urls.extend(img_urls)

        # Include URLs from link tags that point to binary files
        for href in link_urls:
            if binary_patterns.match(href):
                resource_urls.append(href)

        # Resolve and store resource URLs
        for res_url in resource_urls:
            full_res_url = urljoin(response.url, res_url)
            if binary_patterns.match(full_res_url):
                self.resources.append(full_res_url)

        # Extract main text
        main_text = self.extract_main_text(response)
        self.texts.append(main_text)

    def extract_main_text(self, response):
        # Try to find <main> tag content
        main_content = response.css('main')
        if not main_content:
            # Fallback to the largest <div> or <article> tag
            candidates = response.css('div, article')
            if candidates:
                main_content = max(candidates, key=lambda el: len(el.get()), default=None)
            else:
                main_content = None
        else:
            main_content = main_content[0]

        if main_content:
            # Remove script and style tags
            main_content = main_content.xpath('.//*[not(self::script or self::style)]')
            text = main_content.xpath('.//text()').getall()
            text = [t.strip() for t in text if t.strip()]
            text_content = '\n'.join(text)
        else:
            text_content = ''

        return text_content

    def closed(self, reason):
        # Save data to dataframes
        links_df = pd.DataFrame({'url': self.links})
        resources_df = pd.DataFrame({'resource_url': self.resources})
        texts_df = pd.DataFrame({'text': self.texts})

        # Save dataframes to TSV files
        links_df.to_csv('links.tsv', sep='\t', index=False)
        resources_df.to_csv('resources.tsv', sep='\t', index=False)
        texts_df.to_csv('texts.tsv', sep='\t', index=False)

        print("DataFrames have been saved as TSV files.")

# Run the spider
if __name__ == "__main__":
    process = CrawlerProcess({
        'ROBOTSTXT_OBEY': True,
    })
    process.crawl(MySpider)
    process.start()





