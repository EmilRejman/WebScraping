## web srapping
Simple web scrapping project, URL has data in JSON format inside body tag. Get data and parse it from 2 URLS. All code is unittested, integration tests under creation. Testing with pytest module under creation.

made with python 3.7 

##### running the app:
* Create and activate a virtual environment or work on your main one
* Run ``` pip install -r requirements.txt```


###### additional info
*Run "ex2.py" to get results, "test_ex2_class.py" to test the class.*

*With this version we can add users and posts with urls of the same structures without repetitions (automatic removal of duplicates). It still can be optimized for bigger amounts of data.*

*Testing done with unit tests.*

*Data could also be gatherd with e.g. selenium but its not needed in this simple HTML.*

*Task 4 was done with least memory expensive pattern, we could use distance_matrix for faster calculation, but more memory.*

###### coverage:

```
Name                                                        Stmts   Miss  Cover
------------------------------------------------------------------------------
ex2_class.py                                                122      0   100%
test_ex2_class.py                                           187      1    99%
------------------------------------------------------------------------------
TOTAL                                                       316      1    99%
```