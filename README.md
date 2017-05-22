## Rent Reckoner

### Install
The service was written/tested in python 3 ([download link](https://www.python.org/downloads/))

Then you gonna need some python package
```
pip numpy python-dateutil flask
```

### Run
Run this command in the root directory 
```
python ./rent_reckoner/rest.py
```

### Endpoints
|Method|URL|Description|
|-|-|-|
|GET|/habitations/<int:habitant_id>/residents/<int:resident_id>/dept|gives back the resident dept|
|GET|/habitations/<int:habitant_id>/bills|gives back the bills in a ui desider format|
|GET|/habitations/<int:habitant_id>/residents"|gives back the residents in a ui desider format|
|GET|/habitations/<int:habitant_id>/update_depts"|update the residents depths|
|POST|/habitations/<int:habitant_id>/<start>/<end>/<name>|add new resident|

You can test them like
```
curl localhost:5000/habitations/0/update_depts
```

### Modify the input data
You can create your own habitation by just create a json file in `rent-reckoner/data/` with `habitation_` prefix, there is a example file named `rent-reckoner/data/habitation_aradi.json`

The desirable file structure:
```
{
    "id": <int>,
    "residents": [
        {
            "name": <string>,
            "start": <string>, // like "2016-09-01T00:00:00"
            "end": <string>, // like "2017-09-01T00:00:00"
            "paid": <string>, // like "500" (should be int)
            "dept": <int>, // call update_depts endpoint to fill the values
            "id": <int>
        }
    ],
    "bills": [
        {
            "start": <string>, // like "2016-09-01T00:00:00"
            "end": <string>, // like "2016-09-01T00:00:00"
            "type": <string>,
            "amount": <int> // like 500 
        }
    ]
}
```

### UI
To see the bills you need a [rent-reckoner-ui](https://github.com/reveland/rent-reckoner-ui)
