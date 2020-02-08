import PyPDF4 as pdf
import re

docNumPattern = r'^[a-zA-Z]'

#r'(^[a-zA-Z][a-zA-Z]\-[0-9][0-9]\-.*)'
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

        if re.match(re.compile(docNumPattern, flags=re.IGNORECASE),content):
            print("++++ found you ++++")
        else:
            print("-------------------- did not match ------------------")
    #content = " ".join(content.replace(u"\xa0", " ").strip().split())
    return content

def parsePageContent(pageContent):
    content = ""
    lineCount = pageContent.count('\n')
    content = pageContent
    print(lineCount)
    return content