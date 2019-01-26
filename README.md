# Current Issues

## Does not receive complete JSON

```bash
Traceback (most recent call last):
  File "instascrape.py", line 27, in <module>
    data = json.loads(rawData)
  File "/System/Library/Frameworks/Python.framework/Versions/2.7/lib/python2.7/json/__init__.py", line 338, in loads
    return _default_decoder.decode(s)
  File "/System/Library/Frameworks/Python.framework/Versions/2.7/lib/python2.7/json/decoder.py", line 366, in decode
    obj, end = self.raw_decode(s, idx=_w(s, 0).end())
  File "/System/Library/Frameworks/Python.framework/Versions/2.7/lib/python2.7/json/decoder.py", line 382, in raw_decode
    obj, end = self.scan_once(s, idx)
ValueError: Unterminated string starting at: line 1 column 69395 (char 69394)
```

```JSON
{"node":{"comments_disabled":false,"__typename":"GraphVideo","id":"1965616674019237231","edge_media_to_caption":{"edges":[{"node":{"text":">>>\ud83d\ude02 \u041f\u043e\u0434\u043f\u0438\u0441\u044b\u0432\u0430\u0439\u0442\u0435\u0441\u044c \ud83d\ude02<<
```

## Faild to load next page 

```bash
Traceback (most recent call last):
  File "instascrape.py", line 36, in <module>
    for post in data['graphql']['hashtag']['edge_hashtag_to_media']['edges']:
KeyError: 'graphql'
```

```JSON
{
    "message": "Please wait a few minutes before you try again.", 
    "status": "fail"
}
```

# General Scraping Research
https://stackoverflow.com/questions/49085421/scraping-instagram-with-beautifulsoup
https://medium.com/@h4t0n/instagram-data-scraping-550c5f2fb6f1
https://stackabuse.com/download-files-with-python/