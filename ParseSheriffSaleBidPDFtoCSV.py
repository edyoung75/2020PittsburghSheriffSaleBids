'''
Parse the bid_list.pdf Allegheny County Sheriff Sale for Pittsburgh, PA
'''

# IMPORTS
import sys
import csv
import PyPDF4 as pdf
import ParseSheriffSaleBidPDFtoCSVFunctions as fn

content = fn.getPDFContent('./data/bid_list.pdf')
# print the content
print(content)