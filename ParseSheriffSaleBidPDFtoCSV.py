'''
Parse the bid_list.pdf Allegheny County Sheriff Sale for Pittsburgh, PA
'''

# IMPORTS
import sys
import csv
import PyPDF4 as pdf
import ParseSheriffSaleBidPDFtoCSVFunctions as fn
import urllib as url
import requests as req
#import html
from urllib.parse import urlparse

csvHeader = ['Docket #',
             'Attorney Name',
             'Plaintiff Name',
             'Sale Type',
             'Sale Date',
             'CostTax',
             'Cost',
             'Sale Status',
             'PP Date',
             'Reason for PP',
             'Svs',
             '3129',
             'OK',
             'AuctionNo',
             'Defendant Name']

#content = fn.getPDFContent('./data/bid_list.pdf')
# print the content
#print(content)

urlstring = 'http://classified.post-gazette.com/details.asp?id=4107790'
urlstring01 = 'http://classified.post-gazette.com/sheriffsales.asp'

#urlcontent = url.request.urlopen(urlstring)
urlcontent = req.get(urlstring01)
#urlcontent = url.request.urlopen("https://en.wikipedia.org/wiki/Python_(programming_language)")
#urlcontent = url.request.urlopen(urlstring01)
#htmlcontent = urlcontent.read().decode()
#urlcontent.close()
urlparsed = urlparse(urlstring01)
htmlcontent = urlcontent.text
urlcontent.close()

urllist = []
urlscheme = urlparsed.scheme
urlhost = urlparsed.hostname

print(urlparsed.hostname)
#print(urlcontent.text)

from html.parser import HTMLParser

class ParseForLinks(HTMLParser):
    def __init__(self):
        # Since Python 3, we need to call the __init__() function of the parent class
        super().__init__()
        self.reset()

    # Defining what the method should output when called by HTMLParser.
    def handle_starttag(self, tag, attrs):
        # Only parse the 'anchor' tag.

        if tag == "a":
            for name, link in attrs:
                #if name == "href" and link.startswith("http"):
                if name == "href" and link.startswith("/"):
                    #print('http://classified.post-gazette.com{}'.format(link))
                    urllist.append('{}://{}{}'.format(urlscheme, urlhost, link))
                #elif name == "href":
                #    print(link)

p = ParseForLinks()
p.feed(htmlcontent)
# Filter down the list to just URL's with ID in query
urllist = [x for x in urllist if fn.urlFoundInQuery(x, 'id')]
print(urllist)
parsedList = fn.parseForAddresses(urllist)
for row in parsedList:
    print(row)
#print("{} {}".format(urlparsed.scheme, urlparsed.hostname))

addressList = ["810 MAPLE AVE & VACANT LAND, , NORTH VERSAILLES, PA 15137",
               "2600 WOODSTOCK AVE&VACANT LAND, , PITTSBURGH, PA 15218",
               "319 JOHNSTON AVE, , PITTSBURGH, PA 15207",
               "RIDGE RD (VACANT LAND), , BRIDGEVILLE, PA 15017",
               "318 KILBUCK ST, , SEWICKLEY, PA 15143",
               "3330  & 3334  RAINBOW RUN RD, , MONONGAHELA, PA 15063"]

#contentAddresses = fn.addressParseGeoCode(addressList)
#print(contentAddresses)

import urllib
