# StoPy

**HTTP Client + Wrapper for the Sto API [[git](https://github.com/z3dtech/sto)] | [[npm](https://www.npmjs.com/package/sto)]**

Basic python wrapper offering full functionality with the HTTP/HTTPS components of the Sto API

## Installation

```bash
pip install StoPy
```

## Import

```python
from StoPy import StoPy
```

## Initiate

```python
sto = StoPy.StoPy( server='127.0.0.1', port='3000', api_key='api_key_here', protocol='https' ) # enter your auth info here
collection = 'yourcollection' #often a type of data to be stored/fetched
owner = 'yourowner' # often a userid
```

## Store

```python
data = { 'dictionary': 1337 } # stores dictionaries as JSON. 
insert = sto.insert(collection, owner, data ) # uploads to server
```

## Fetch

```python
lastInsert = sto.readLatest(collection,owner,limit=1) # returns list of inserts if limit > 1
firstInsert = sto.readOldest(collection,owner,limit=1) # otherwise returns object
lastInsertedPaginated = sto.readOldestByPage(collection, owner, items_per_page=2, page_number=1 ) # 0 indexed pages
firstInsertedPaginated = sto.readLatestByPage(collection, owner, items_per_page=2, page_number=1 ) # 0 indexed pages
count = sto.getCount(collection,owner) # returns count of total records stored
hashData = firstInsertedPaginated['data'][0]['hashData']
hashRead = sto.readHash(collection,hashData) # store/read hash to fetch individual records
```

## Delete


```python
hashDelete = sto.deleteByHash(collection,hashData) # delete individual records
ownerDeleteAll = sto.deleteByOwner(collection,owner,save=2) # delete all records by owner (except last 2)
ownerDeleteAll = sto.deleteByOwner(collection,owner) # delete all records by owner
```
