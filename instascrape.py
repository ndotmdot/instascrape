from bs4 import BeautifulSoup
import requests
import time
import json
import datetime
import wget

tagToScrape = 'selfie'
pagesToScrape = 300 # one page has about 60 items

exportImg = False 
exportMeta = False # save all post related data as json

exportSoup = True # helpful for debugging
exportRawData = True # same same
exportGraphQl = True # same same

nextPageSlug = ''
imageCount = 0

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

for page in range(pagesToScrape):        
    url = 'https://www.instagram.com/explore/tags/' + tagToScrape + '/?__a=1' + nextPageSlug
    validSoup = False
    validRawData = False
    validGraphQl = False

    print('\n\nRequesting graphQl for page number ' + str(page + 1) + '...\nfrom url: ' + url + '\n')

    while validSoup is False or validRawData is False or validGraphQl is False:
        r = requests.get(url, timeout=20)
        
        soup = BeautifulSoup(r.text, 'lxml')
        if str(soup).startswith('<html>') and str(soup).endswith('</html>'):
            validSoup = True
            print("Valid soup: " + str(validSoup))
        else:
            print("Error: Valid soup: " + str(validSoup))
            r = None
            waitFor(5)
        if exportSoup:
            exportText(soup,'-' + str(tagToScrape ) + '-Soup', 'txt', './_pageData/')

        rawData = soup.find('p').contents[0]
        if str(rawData).startswith('{') and str(rawData).endswith('}'):
            validRawData = True
            print("Valid raw data: " + str(validRawData))
        else:
            print("Error: Valid raw data: " + str(validRawData))
            rawData = str(soup.find('p').contents[0]) + '"}}]}}}]}}}}'
            validRawData = True
        if exportRawData:
            exportText(rawData,'-' + str(tagToScrape ) + '-RawData', 'txt', './_pageData/')

        data = json.loads(rawData)
        if 'graphql' in data:
            validGraphQl = True
            print("Valid graphql: " + str(validGraphQl))
        else:
            print("Error: Valid graphql: " + str(validGraphQl))
            waitFor(30)
        if exportGraphQl:     
            exportText(str(json.dumps(data, sort_keys=True, indent=4)),'-' + str(tagToScrape ) + '-GraphQl', 'json', './_pageData/')


    for post in data['graphql']['hashtag']['edge_hashtag_to_media']['edges']:    
        id = post['node']['id']
        print('\nFetching ' + tagToScrape + ' number ' + str(imageCount) + " with image-id " + str(id) + ' from page ' + str(page + 1) + '...')

        if exportImg:
            # print('Downloading...')
            image_src = post['node']['thumbnail_resources'][4]['src']
            wget.download(image_src, './_img/'+ str(id) +'_img.jpg')

        if exportMeta:
            # print('\nSaving Metadata...')
            meta = post['node']
            source = open('./_meta/'+ str(id) +'_meta.json', 'w')
            source.seek(0)
            source.write(str(json.dumps(meta, sort_keys=True, indent=4)))

        imageCount = imageCount + 1

    nextPageSlug = '&max_id=' + data['graphql']['hashtag']['edge_hashtag_to_media']['page_info']['end_cursor']


