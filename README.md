# Instascrape
Simple python scripts to download instagram images by tag or user name.

## Usage

### Scrape by Tag
1. Change tag in line 9 in `scrape_by_tag.py'
2. Run script in directory

```bash
python scrape_by_tag.py
```


### Scrape by User
1. Change username in line 8 in `scrape_by_user.py'
2. Run script in directory

```bash
python scrape_by_user.py
```

### Options:
```bash
exportMeta = False # save all post related data as json
exportSoup = False # helpful for debugging
exportRawData = False # same same
exportGraphQl = False # same same
```

## Requirements
* Python 3
* Beautyfull Soup
* Wget