from bs4 import BeautifulSoup
import requests
import json
import datetime
import wget

tagToScrape = 'selfie'
pagesToScrape = 300; # one page has about 60 items

isExportImg = True 
isExportMeta = True # save all post related data as json

isExportRawData = True # helpful for debugging
isExportGraphQl = True # same same

nextPageSlug = ''
imageCount = 0

for page in range(pagesToScrape):
        
        
    print('\n \n \n Allright, requesting graphQl for ' + str(page) + '...')
    r = requests.get('https://www.instagram.com/explore/tags/' + tagToScrape +'/?__a=1' + nextPageSlug)
    soup = BeautifulSoup(r.text, 'lxml')
    rawData = soup.find('p').contents[0]

    if isExportRawData is True:

        filename = 'tag-' + str(tagToScrape) + datetime.datetime.now().strftime('-date-%d-%m-%Y-time-%H-%M-%S')
        source = open('./_pageData/' + filename +'.txt', 'w')
        source.seek(0)
        source.write(rawData)

    data = json.loads(rawData)

    if isExportGraphQl is True:
        
        filename = 'tag-' + str(tagToScrape) + datetime.datetime.now().strftime('-date-%d-%m-%Y-time-%H-%M-%S')
        source = open('./_pageData/' + filename +'.json', 'w')
        source.seek(0)
        source.write(str(json.dumps(data, sort_keys=True, indent=4)))

    for post in data['graphql']['hashtag']['edge_hashtag_to_media']['edges']:
        
        id = post['node']['id']
        print('\nScraping on page ' + str(page) + '. Fetching ' + tagToScrape + ' number ' + str(imageCount) + " with image-id " + str(id))

        if isExportImg is True:

            print('Downloading...')
            image_src = post['node']['thumbnail_resources'][4]['src']
            wget.download(image_src, './_img/'+ str(id) +'_img.jpg',)

        if isExportMeta is True:

            print('\nSaving Metadata...')
            meta = post['node']
            source = open('./_meta/'+ str(id) +'_meta.json', 'w')
            source.seek(0)
            source.write(str(json.dumps(meta, sort_keys=True, indent=4)))

        imageCount = imageCount + 1

    nextPageSlug = '&max_id=' + data['graphql']['hashtag']['edge_hashtag_to_media']['page_info']['end_cursor']



