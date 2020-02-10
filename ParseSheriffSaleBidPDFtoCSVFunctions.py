import PyPDF4 as pdf
import geocoder
import urllib
import json
import re

docNumPattern = re.compile(r'\w{2}-\w{2}-\w{6}')
auctionNumPattern = re.compile(r'\d{3}\w{3}\d{2}')
endOfPagePattern = re.compile('^Report.*')
possibleSaleTypesHas2ndLine = 0
possibleSaleTypesWith2ndLine = ['Sci Fa sur Tax ',
                                'Mortgage ',
                                'Other Real ']

possibleSaleTypes2ndLine = ['Lien',
                            'Foreclosure',
                            'Estate']
possibleSaleTypesOnly1Line = ['Municipal Lien']
ignoreList = ['Docket #',
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

saleTypesWODatesList = ['ACTIVE',
                 'STAYED']

# Function returns a list of dockets and contents organized into another list
def getPDFContent(path):
    file = open(path, "rb")
    fileReader = pdf.PdfFileReader(file)
    numPages = fileReader.getNumPages()

    # Master List
    contentList = []

    # Iterate through the pages of the PDF
    for i in range(0, numPages):
        tContent = fileReader.getPage(i).extractText()
        tContentList = []
        # Parse a single page for all the dockets
        tContentList = parsePageContent(tContent)
        # Since the contents are nested lists, pull them out and put them into a the master list
        for col in tContentList:
            contentList.append(col)

    # Return the final Master list
    return contentList

docketNum = ""
docketContentList = []

def parsePageContent(pageContent):
    content = ""
    lineCount = pageContent.count('\n')
    print(lineCount)
    print("\n================ Content ===============\n")
    chunks = pageContent.split('\n')
    #print(chunks)

    global docketNum
    global docketContentList

    docketInitialContents = []
    docketListCount = 0
    tempContentStr = ""

    tPostponeTrigger = ""
    tCommentTrigger = ""

    for col in chunks:
        # find the docket #
        print(docketListCount)
        if docNumPattern.match(col):
            # Clear any content that isn't associated with a docket
            # Also set the
            if docketNum == "":
                docketContentList = []
                tempContentStr = ""
                docketNum = col
                docketContentList.append(col)
                docketListCount = 0

            # If another docket # is found and there is another docket already, then the system must have found all the elements of the previous docket
            # Update the docketDictionary with all the new docket information.
            else:
                #add the previous docket to the docketDictionary
                #docketDictionary.update({docketNum : docketContentList})
                docketInitialContents.append(docketContentList)
                print(docketContentList)
                docketContentList = []
                docketNum = col
                docketContentList.append(col)
                #resets the docketListCount back to 0
                docketListCount = 0

            print("Found a Docket #" + docketNum)

        elif col in possibleSaleTypesOnly1Line:
            docketContentList.append(tempContentStr)
            docketContentList.append(col)
            tempContentStr = ""
            docketListCount += 1
        elif col in possibleSaleTypesWith2ndLine:
            docketContentList.append(tempContentStr)
            docketListCount += 1
            tempContentStr = col
            #print(tempContentStr)
            #print(docketListCount)
        elif col in possibleSaleTypes2ndLine:
            tempContentStr = tempContentStr + col
            docketContentList.append(tempContentStr)
            tempContentStr = ''
            docketListCount += 1
            print("[[[[[ salmon ]]]]]")
        elif docketListCount == 1:
            #Add the col to the temp string rather than the docketContentList
            tempContentStr = tempContentStr + col
            # print(docketListCount)
            print("[[[[[ tuna ]]]]]")

        # found the last item on the page
        elif endOfPagePattern.match(col):
            # Update the dictionary
            #docketDictionary.update({docketNum : docketContentList})
            docketInitialContents.append(docketContentList)
            # Hit the last item on the page so wipe all existing content
            #docketNum = ""
            #docketContentList = []
            #docketDictionary = {}
            tempContentStr = ""
            #print("hit the end of the page " + col)
            #docketListCount = 0
            break
        elif col in ignoreList:
            # Do nothing with the info
            print("Ignoring "+col)

        elif col in saleTypesWODatesList:
            docketContentList.append(col)
            docketContentList.append(" ")
            docketListCount += 2

        # Auction Date Match
        elif auctionNumPattern.match(col):
            print("[[[[[ Auction ]]]]]")
            for i in range(docketListCount,11):
                docketContentList.append("O")
                docketListCount +=1
            docketContentList.append(col)
            docketListCount += 1

        elif tCommentTrigger and col == chunks[-1]:
            #tCommentTrigger = tCommentTrigger + " " + col
            #docketContentList.append(tCommentTrigger)
            #tCommentTrigger = ""
            print(chunks[-1])
            docketContentList.append(col)
        elif tCommentTrigger:
            #tCommentTrigger = tCommentTrigger + " " + col
            print("Something triggered")
            docketContentList.append(col)
        elif col == "Comments:" and col == chunks[-1]:
            #tCommentTrigger = col
            #docketContentList.append(tCommentTrigger)
            #tCommentTrigger = ""
            print("crap")
            docketContentList.append(col)
        elif col == "Comments:":
            #tCommentTrigger = col
            print("snapper")
            docketContentList.append(col)
        elif docketListCount == 14:
            print(col)

            docketContentList.append(col)
        else:
            docketContentList.append(col)
            docketListCount += 1
            #print("ADDING to the Content List ")
            #print(docketContentList)

    print(docketContentList)
    if not docketContentList:
        docketInitialContents.append(docketContentList)
    #print(docketInitialContents)

    return docketInitialContents


# Function checks if the string
# contains any special character
def run(string):
    # Make own character set and pass
    # this as argument in compile method
    regex = re.compile('[@_!#$%^&*()<>?/\|}{~:]')

    # Pass the string in search
    # method of regex object.
    if (regex.search(string) == None):
        print("String is accepted")

    else:
        print("String is not accepted.")

featurePropertiesExample = {'address': '318 Kilbuck St, Sewickley, Pennsylvania, 15143',
                  'bbox': [-80.1305425, 40.521311000000004, -80.1285425, 40.523311],
                  'confidence': 9,
                  'lat': 40.52233455314792,
                  'lng': -80.13029678746658,
                  'ok': True,
                  'quality': 'PointAddress',
                  'raw': {'name': '318 Kilbuck St, Sewickley, Pennsylvania, 15143',
                          'extent': {'xmin': -80.1305425,
                                     'ymin': 40.521311000000004,
                                     'xmax': -80.1285425,
                                     'ymax': 40.523311},
                          'feature': {'geometry': {'x': -80.13029678746658, 'y': 40.52233455314792},
                                      'attributes': {'Score': 100, 'Addr_Type': 'PointAddress'}}},
                  'score': 100,
                  'status': 'OK'}

def geoCodeCoord(address):
    # initialize your variable to None
    lat_lng_coords = None
    # loop until you get the coordinates
    while (lat_lng_coords is None):
        # ArcGIS gives a Dictionary response
        g = geocoder.arcgis(address)
        #print(g.geojson.keys())
        featureAddress = g.geojson['features'][0]['properties']['address']
        featureLat = g.geojson['features'][0]['properties']['lat']
        featureLng = g.geojson['features'][0]['properties']['lng']
        print(featureAddress)
        lat_lng_coords = [featureLat, featureLng, featureAddress]
    latitude = lat_lng_coords[0]
    longitude = lat_lng_coords[1]
    addressUsed = lat_lng_coords[2]
    return latitude, longitude, addressUsed

def addressParseGeoCode(addresses):
    content = []
    tAddressList = []
    for col in addresses:
        print('Working on addresses...')
        #addyURL = urllib.parse.quote_plus(col)
        addyURL = col
        print(addyURL)
        latitude, longitude, addressUsed = geoCodeCoord(addyURL)
        tAddressList.append(col)
        print(latitude)
        print(longitude)
        #tAddressList.append(latitude + ", " + longitude)
        content.append(tAddressList)
        tAddressList =[]
    return content