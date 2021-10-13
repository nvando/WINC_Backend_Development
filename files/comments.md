## Creating files/folders in the 'current working directory'

The 'current working directory' can change depending on the directory that python is invoked from. 
If you want to create files or folders in the same directory as the script you are writing, 
you could also use use function that retrieves the absolute path of the directory in which the code that you are writing is stored.

Request directory of current script with:
```
SCRIPT_DIRECTORY = pathlib.Path(__file__).parent.absolute()
```


```__file__``` is the full absolute name of the script currently running.    
` `  
` `
With the below code you could then create a path which is relative to the script location, thus using the script location as anchor point to retrieve or create other files.   

```
file_path = SCRIPT_DIRECTORY / "file.zip"
```


