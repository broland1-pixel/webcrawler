#Webcrawler

[![Python 3.6](https://img.shields.io/badge/python-3.6-blue.svg)](https://www.python.org)

This is a simple web scraper that finds and counts the urls on a series of page.   

First, it crawls the site and adds those urls to a list of urls to be scraped, and then calls the scraper.

It uses Beautiful Soup to parse the web page and find the urls.  
It then uses the urllib.parse to combine the relative urls found on the page.  

It outputs the urls in a txt file, with the following format: url, url_count,