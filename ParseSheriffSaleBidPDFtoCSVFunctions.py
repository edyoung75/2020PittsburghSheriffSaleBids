import PyPDF4 as pdf
import re

docNumPattern = re.compile(r'\w{2}-\w{2}-\w{6}')
endOfPagePattern = re.compile('^Report.*')

def getPDFContent(path):
    content = ""
    file = open(path, "rb")
    fileReader = pdf.PdfFileReader(file)
    numPages = fileReader.getNumPages()
    print(numPages)
    for i in range(0, numPages):
        tContent = fileReader.getPage(i).extractText()
        tContent = parsePageContent(tContent)

        content += tContent + "\n"

    #content = " ".join(content.replace(u"\xa0", " ").strip().split())
    return content

def parsePageContent(pageContent):
    content = ""
    lineCount = pageContent.count('\n')
    print(lineCount)
    print("\n================ Content ===============\n")
    chunks = pageContent.split('\n')
    print(chunks)
    docketNum = ""
    docketContentList = []
    docketDictionary = {}
    docketListCount = 0
    docketPlaintiffName = []
    for col in chunks:
        if docNumPattern.match(col):
            # Clear any content that isn't associated with a docket
            # Also set the
            if docketNum == "":
                docketContentList = []
                docketNum = col
                docketListCount += 1

            # If another docket # is found and it's not empty, then the system must have found all the elements of the docket
            # Update the docketDictionary with all the new docket information.
            else:
                docketDictionary.update({docketNum : docketContentList})
                docketContentList = []
                docketNum = col
            print("found a Docket #" + docketNum)
        elif endOfPagePattern.match(col):
            # Update the dictionary
            docketDictionary.update({docketNum : docketContentList})
            # Hit the last item on the page so wipe all existing content
            docketNum = ""
            docketContentList = []
            docketDictionary = {}
            #print("hit the end of the page " + col)
            break
        else:
            docketContentList.append(col)
            #print("ADDING to the Content List ")
            print(docketContentList)

    print(docketDictionary)
    content = pageContent

    return content


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