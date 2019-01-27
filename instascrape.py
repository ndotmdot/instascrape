from bs4 import BeautifulSoup
import requests
import time
import json
import datetime
import wget

tagToScrape = 'selfie'
pagesToScrape = 300 # one page has about 60 items

exportImg = True 
exportMeta = True # save all post related data as json

exportSoup = False # helpful for debugging
exportRawData = False # same same
exportGraphQl = False # same same

# Helper functions

def waitFor( timeIn ):
    print('Waiting for ' + str(timeIn) + ' seconds...')
    for i in xrange(timeIn,0,-1):
        time.sleep(1)
        print(i)

def exportText(fileData, fileName, fileExtension, filePath):
    filename = datetime.datetime.now().strftime('date-%d-%m-%Y-time-%H-%M-%S') + fileName
    source = open(filePath + filename + '.' + fileExtension, 'w')
    source.seek(0)
    source.write(str(fileData))

# Main programm

brokenPageRequests = 0
imagesDownloaded = 0
nextPageSlug = ''
imageCount = 0

for page in range(pagesToScrape):   
    print('\n\nTotal images downloaded: ' + str(imagesDownloaded))
    print('Total pages scraped:  ' + str(page) + ' of ' + str(pagesToScrape))
    print('Broken page requests:  ' + str(brokenPageRequests))

    url = 'https://www.instagram.com/explore/tags/' + tagToScrape + '/?__a=1' + nextPageSlug
    validSoup = False
    validRawData = False
    validGraphQl = False

    print('Requesting graphQl for page number ' + str(page + 1) + '...\nfrom url: ' + url + '\n')

    while validSoup is False or validRawData is False or validGraphQl is False:
        r = requests.get(url, timeout=20)
        
        soup = BeautifulSoup(r.text, 'lxml')
        if str(soup).startswith('<html>') and str(soup).endswith('</html>'):
            validSoup = True
            print("Valid soup: " + str(validSoup))
        else:
            print("Error: Valid soup: " + str(validSoup))
        if exportSoup:
            exportText(soup,'-' + str(tagToScrape ) + '-Soup', 'txt', './_pageData/')

        rawData = soup.find('p').contents[0]
        if str(rawData).startswith('{') and str(rawData).endswith('}'):
            validRawData = True
            print("Valid raw data: " + str(validRawData))
        else:
            print("Error: Valid raw data: " + str(validRawData))
            print("Warning: Fixing data. Some data will be lost.")
            rawData = str(soup.find('p').contents[0]) + '"}}]}}}]}}}}'
            validRawData = True
            brokenPageRequests = brokenPageRequests + 1
        if exportRawData:
            exportText(rawData,'-' + str(tagToScrape ) + '-RawData', 'txt', './_pageData/')

        data = json.loads(rawData)
        if 'graphql' in data:
            validGraphQl = True
            print("Valid graphQl: " + str(validGraphQl))
        else:
            print("Error: Valid graphQl: " + str(validGraphQl))
            waitFor(30)
        if exportGraphQl:     
            exportText(str(json.dumps(data, sort_keys=True, indent=4)),'-' + str(tagToScrape ) + '-GraphQl', 'json', './_pageData/')


    for post in data['graphql']['hashtag']['edge_hashtag_to_media']['edges']:    
        id = post['node']['id']
        print('\nFetching #' + tagToScrape + ' number ' + str(imageCount) + ' from page ' + str(page + 1) + '...')

        if exportImg:
            if 'thumbnail_resources' in post['node']:
                print('Downloading...')
                image_src = post['node']['thumbnail_resources'][4]['src']
                wget.download(image_src, './_img/'+ str(id) +'.jpg')
                imagesDownloaded = imagesDownloaded + 1
            else:
                print('Warning: graphQl was damaged, can not download.image...')

        if exportMeta:
            if 'thumbnail_resources' in post['node']:
                print('\nSaving Metadata...')
                meta = post['node']
                exportText(str(json.dumps(meta, sort_keys=True, indent=4)),'-' + str(tagToScrape ) + '-meta', 'json', './_meta/')

            else:
                print('Warning: graphQl was damaged, can not save data...')
           

        imageCount = imageCount + 1

    nextPageSlug = '&max_id=' + data['graphql']['hashtag']['edge_hashtag_to_media']['page_info']['end_cursor']


