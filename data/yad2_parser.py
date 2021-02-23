import requests
from bs4 import BeautifulSoup
import typing

from time import sleep
from random import uniform


class Not200StatusCode(Exception):
    pass


class Parser:
    """
    Basic yad2.co.il parser, data parsing (apartment rentals) for the specified parameters
    Makes request to the site, parses the data, saves data to a list
    """
    base_url = 'https://www.yad2.co.il/vehicles/private-cars'
    manufacturer_url = '?manufacturer='
    model_url = '&model='
    group_color = '&group_color='
    pages_url = '&page={page_number}'
    year = '&year='

    def __init__(self, keywords, is_paginate=True, url=True):
        self.classification = keywords[1]
        self.keywords = keywords
        self.is_paginate = is_paginate
        self.url = url
        self.data = []

    def _make_url(self, keywords):
        """
        Generates a url based on parsing parameters.
        :param keywords: numbers of rooms, price, floor
        :return: url ready for parsing
        """
        # Adds url's with keywords to the base url
        self.url = self.base_url + self.manufacturer_url + str(keywords[0]) \
                   + self.model_url + str(keywords[1]) \
                   + self.group_color + str(keywords[2]) \
                   + self.year + str(keywords[3])
        return self.url

    def _pagination(self, page_number, pages_url):
        """
        Generates the url of the next page and sends a request to the site.
        :param page_number:
        :return: content html
        """
        url = self._make_url(keywords=self.keywords)
        url_pagination = url + pages_url.format(page_number=page_number)
        headers = {
            'Host': 'www.yad2.co.il',
            'Connection': 'keep-alive',
            'Pragma': 'no-cache',
            'Cache-Control': 'no-cache',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'Sec-Fetch-Site': 'none',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-User': '?1',
            'Sec-Fetch-Dest': 'document',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'en-US,en;q=0.9',
            'Cookie': 'recommendations-searched-vehicles=true; __uzma=c7cadb83-d6ce-4987-aa67-3c469736ca18; __uzmb=1612516098; __uzme=8743; abTestKey=41; _ga=GA1.3.371937583.1612516101; leadSaleRentFree=57; use_elastic_search=1; __ssds=3; __ssuzjsr3=a9be0cd8e; __gads=ID=48d4ec304510c4bf:T=1612516102:S=ALNI_MZSXiVO5ZMKNss0JZwHi9rENuabGg; _fbp=fb.2.1612516103733.821674275; _hjTLDTest=1; _hjid=1d400ae0-6bd4-41bb-adce-a6031b2330ed; bc.visitor_token=6742332496341942272; __uzmaj3=0679bf7e-912b-47fc-8545-73cdc585fcda; __uzmbj3=1612519564; canary=never; _gid=GA1.3.1121440698.1613126801; server_env=production; y2_cohort_2020=17; y2018-2-cohort=69; _hjIncludedInSessionSample=1; __uzmcj3=674293464901; __uzmdj3=1613153118; __uzmd=1613153120; __uzmc=2457380595843; favorites_userid=bjc320620000'
        }
        response = requests.get(url_pagination, headers=headers)
        return response.content

    def _pars_block(self, blocks):
        """
        Splits the page content into blocks
        Generates a dictionary for each data block and saves them to a list.
        :param blocks: the content of the page
        :return: list of data
        """
        sleep(uniform(5, 8))
        data = []
        counter = 0
        for block in blocks:
            image_url = block.find('img', class_='feedImage')
            car_name = block.find('span', class_='title')
            adress_block = block.find('div', class_='rows')

            #             rooms_floor_area_block = block.find('div', class_='middle_col')
            #             price_block = block.find('div', class_='price')
            #             date_added_block = block.find('span', class_='date')

            # to do according to what returns
            d = {
                'id': counter,
                'img_url': image_url['src'],
                'car_name': adress_block.get_text(),
                'car_name2': car_name.get_text(),
                'classification': self.classification
            }
            print("car type: ", d["car_name2"])
            counter = counter + 1

            data.append(d)
        return data

    def parse_content(self, content, page_number=2):
        """
        Recursive method.
        Gets content (blocks), parser it and saves the information to a list.
        Checks for pagination, parses the following pages.
        :param page_number:
        :param content: html
        :return: list of data
        """
        sleep(uniform(8, 15))

        soup = BeautifulSoup(content, 'html')

        # print(soup)

        blocks = soup.find_all('div', class_='feed_item feed_item-v4 accordion desktop')

        print("blocks:", len(blocks))

        data = self._pars_block(blocks)
        self.data.extend(data)
        print('INFO: already parsed {} blocks'.format(len(self.data)))

        sleep(uniform(3, 8))

        sleep(uniform(3, 8))

        # print(data)

        sleep(uniform(8, 15))

        # find the button 'next' that is not active in the pagination
        paginated_block = soup.find('div', class_='pagination clickable')
        button_next = paginated_block.find('button', class_='page-num current-page-num')
        print('Next button: ', button_next)  # None

        # if pagination is enabled and button next is active
        if self.is_paginate and not button_next:
            sleep(uniform(8, 15))
            print('INFO: Try to paginate page number ', page_number)
            # get the content of the next page
            content = self._pagination(page_number, pages_url=self.pages_url)

            self.parse_content(content, page_number + 1)

        return self.data

    def send_request(self, url):
        """
        The method generates and sends a request to the site.
        Calls the sleep method to avoid being banned.
        :param url: url with search parameters
        :return: html content
        """
        sleep(uniform(3, 8))

        print('INFO: url is ', url)

        headers = {
            'Host': 'www.yad2.co.il',
            'Connection': 'keep-alive',
            'Pragma': 'no-cache',
            'Cache-Control': 'no-cache',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'Sec-Fetch-Site': 'none',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-User': '?1',
            'Sec-Fetch-Dest': 'document',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'en-US,en;q=0.9',
            'Cookie': 'recommendations-searched-vehicles=true; __uzma=c7cadb83-d6ce-4987-aa67-3c469736ca18; __uzmb=1612516098; __uzme=8743; abTestKey=41; _ga=GA1.3.371937583.1612516101; leadSaleRentFree=57; use_elastic_search=1; __ssds=3; __ssuzjsr3=a9be0cd8e; __gads=ID=48d4ec304510c4bf:T=1612516102:S=ALNI_MZSXiVO5ZMKNss0JZwHi9rENuabGg; _fbp=fb.2.1612516103733.821674275; _hjTLDTest=1; _hjid=1d400ae0-6bd4-41bb-adce-a6031b2330ed; bc.visitor_token=6742332496341942272; __uzmaj3=0679bf7e-912b-47fc-8545-73cdc585fcda; __uzmbj3=1612519564; canary=never; _gid=GA1.3.1121440698.1613126801; server_env=production; y2_cohort_2020=17; y2018-2-cohort=69; _hjIncludedInSessionSample=1; __uzmcj3=674293464901; __uzmdj3=1613153118; __uzmd=1613153120; __uzmc=2457380595843; favorites_userid=bjc320620000'
        }

        response = requests.get(url, headers=headers)

        if not response.status_code == 200:
            raise Not200StatusCode('Status code is: ', response.status_code)

        print('INFO: Status code is 200')
        # print(response.content)

        return response.content

    def start(self, keywords):
        self.keywords = keywords
        self.classification = keywords[1]
        self.data = []
        """
        Calls methods of the class.
        :param keywords: numbers of rooms, price, floor
        :return:
        """
        url = self._make_url(keywords)
        html_content = self.send_request(url)

        data = self.parse_content(html_content)
        print('LEN DATA: ', len(data))

        return data