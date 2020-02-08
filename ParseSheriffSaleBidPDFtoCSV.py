'''
Parse the bid_list.pdf Allegheny County Sheriff Sale for Pittsburgh, PA
'''

# IMPORTS
import sys
import csv
import PyPDF4 as pdf
import ParseSheriffSaleBidPDFtoCSVFunctions as fn

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

content = fn.getPDFContent('./data/bid_list.pdf')
# print the content
print(content)