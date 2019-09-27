# simpleDB
A simple in-memory key/value store with support for transaction blocks

## Getting Started
CLI prompt for the simpleDB is implemented using Python's cmd package. This includes support for the leading '>'. 
To invoke the prompt:
```
$ python simpleDB.py
...Simple Key/Value Store...
...Type help for options...
> SET key1 7
> GET key1
7
> 
``` 

List of supported commands can be accessed by typing help or help [command]:
```
> help DELVALUE

        Delete Keys with given Value in Store
        
> 
```

simpleDB supports transaction block execution throuigh MULTI, DISCARD and EXEC
```
> MULTI
> SET k 1
> INCR k
> DISCARD
2
> SET k 10
> EXEC
1
> GET k
10
```
### Testing
simpleDB was developed using python 2.7.15. Unit testing was implemented using unittest package along with StringIO for CLI. 
Overall testing strategy was to use file based tests with input commands and expected output. 
To invoke tests:
```
$ python test_db.py
```
The tests are located under ./data directory. 

### Supported Commands
The following limited command set is supported:
__BASIC__:
	* __GET [key]__ : Get integer value corresponding to the key. Returns <nil> if key does not exist
	* __SET [key] [value]__: Set key to hold integer value
	* __INCR [key]__: Increments number stored at key by 1. If it doesn't exist, the value of 0 is set before incrementing
	* __DEL [key]__: Removes the specified key
	* __DELVALUE [value]__: Removes all keys that have the specified value

__TRANSACTIONAL__:
	* __MULTI__ : Marks start of a transaction block
	* __DISCARD__: Flushes all queued commands without changing data, Prints NOT IN TRANSACTION if queue is empty
	* __EXEC__: Commits previously queued commands. Prints NOT IN TRANSACTION if queue is empty

### Assumptions
* Nested transaction blocks are not supported. 
* The correctness of the input command is assumed. If SET command is missing value, the user will be prompted:
```
> SET k
missing key/value
```

### Further improvements
* __DELVALUE__: This transaction will be much faster if there is a hashmap of values that contain list of keys. The tradeoff is increase in space complexity for ___almost___ constant time deletions.
* __Nested Transaction Blocks__: This can be supported with further tweaks to the data store.  
