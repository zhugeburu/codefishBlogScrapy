# -*- coding: utf-8 -*-
import re
import requests
import scrapy
import json
from scrapy import Request
import time
from codefish.items import CodefishItem




class codefishSpider(scrapy.Spider):
    name = "codefish"
    allowed_domains = ["www.cnblogs.com"]
    start_urls = (
        "http://www.cnblogs.com/codefish/default.html?page=%d" % i for i in range(1,9)
    )

    def __init__(self):
        self.s = requests.session()

    def parse(self, response):
        reqs = []
        for sel in response.css('div.forFlow > .day'):
            url = sel.css('div.postTitle > a::attr(href)').extract_first()
            print ('Scraping link ' + url)
            req = Request(url=url,callback=self.parse_item)
            reqs.append(req)
        return reqs

    def get_visit_count(self,post_id):
        url = "http://www.cnblogs.com/mvc/blog/ViewCountCommentCout.aspx?postId=" + str(post_id)
        response = self.s.get(url)
        return int(response.text)

    def parse_result(self,response):
        # return response.body
        return 11

    def get_comments_count(self,post_id):
        now = time.time() * 1000
        url = "http://www.cnblogs.com/mvc/blog/GetComments.aspx?" \
              "postId=%s&blogApp=codefish&pageIndex=0&anchorCommentId=0&_=%d" % (post_id,now)
        # Request(url,callback=self.parse_comment)
        r = self.s.get(url)
        return int(json.loads(r.text)['commentCount'])

    def parse_comment(self,response):
        # return json.loads(response.body)['commentCount']
        # return re.findall(r'"commentCount":(\d){,2},"commentsHtml"',response.url)[0]
        return 11


    def parse_item(self,response):
        item = CodefishItem()
        print 'Parse Url ' + response.url
        post_id =  response.url[-12:-5]
        item['title'] = response.css('h1.postTitle > a::text').extract_first()
        item['post_time'] = response.css('#post-date::text').extract_first()
        item['author'] = response.css('div.postDesc > a:nth-child(2)::text').extract_first()
        item['visit'] = self.get_visit_count(post_id)
        # item['visit'] = 11
        item['comment'] = self.get_comments_count(post_id)
        # item['comment'] = 11
        try:
            print repr(item).decode("unicode-escape") + '\n'
        except UnicodeEncodeError:
            print u'解码发生错误'
        return item


