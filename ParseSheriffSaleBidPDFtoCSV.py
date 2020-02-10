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

addressList = ["810 MAPLE AVE & VACANT LAND, , NORTH VERSAILLES, PA 15137",
               "2600 WOODSTOCK AVE&VACANT LAND, , PITTSBURGH, PA 15218",
               "319 JOHNSTON AVE, , PITTSBURGH, PA 15207",
               "RIDGE RD (VACANT LAND), , BRIDGEVILLE, PA 15017",
               "318 KILBUCK ST, , SEWICKLEY, PA 15143",
               "3330  & 3334  RAINBOW RUN RD, , MONONGAHELA, PA 15063"]

contentAddresses = fn.addressParseGeoCode(addressList)
print(contentAddresses)