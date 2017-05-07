## Rent Reckoner

### Install
The service was written/tested in python 3 ([download link](https://www.python.org/downloads/))

### Run
Run this command in the root directory 
```
python ./rent_reckoner/rest.py
```
 
### Endpoints
|URL|Des|
|-|-|
|/dept/<int:resident_id>|gives back the resident dept|
|/bills|gives back the bills in a ui desider format|

You can test them like
```
curl localhost:5000/dept/1
```

### Modify the input data
You can modify any data in `rent-reckoner/data/bills.json` and `rent-reckoner/data/residents.json`. Restart is not necessary.

### UI
[rent-reckoner-ui](https://github.com/reveland/rent-reckoner-ui)
