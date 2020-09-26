import requests
import re
import urllib.parse as urlparse
from bs4 import BeautifulSoup

class Scanner:
    def __init__(self,url):
        self.target_url = url
        self.target_links = []
    def extractLinks(self,url):
        response = requests.get(url)
        return re.findall('(?:href=")(.*?)"', response.content.decode())
    def crawl(self,url=None):
        if url == None:
            url = self.target_url
        links = self.extractLinks(url)
        for link in links:
            link = urlparse.urljoin(url, link)

            if "#" in link:
                link = link.split("#")[0]

            if self.target_url in link and link not in self.target_links:
                self.target_links.append(link)
                print (link)
                self.crawl(link)

    def extract_forms(self,url):
       response = self.session.get(url)
       parsed_html = BeautifulSoup(response.content)
       return parsed_html.findAll("form")
    def submit_form(self,form,value,url):
        action = form.get("action")
        post_url = urlparse.urljoin(url,action)
        method = form.get("method")
        inputs = form.findAlll("input")
        post_data = {}
        for input in inputs:
            input_name = input.get("name")
            input_type = input.get("type")
            input_value = input.get("value")
            if input_type == "text":
                input_value = value

            post_data[input_name] = input_value
        if method == "post":
            return self.session.post(post_url,data=post_data)
        return  self.session.get(post_url, params=post_data)
