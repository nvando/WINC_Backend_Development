
# SuperPy 


The following three technical elements have been built into SuperPy to help solve issues with input data validation, testing of functions and reusibility of the code.



**1. Argparse subparsers** 

In order to generate solid and reliable reports from data, it is important to limit any missing data fields and erroneous data. Instead of letting the user deal with this kind of data by having him/her clean-up incomplete or inaccurate datasets, this program peforms checks when data is entered into the database. This prevents missing data fields or data of the wrong type from ending up in the database in the first place. 
In SuperPy, subparsers are used to perform these checks on all data that entered through the CLI. Each sub-command in this program requires a unique set of arguments and the subparsers allow the program to distinguish between them. This means that for each individual command,  different required and optional arguments were set, which are all validated for type. 

For instance, the 'buy' command prompts the user to always enter a product-name, buy-price and expiration date, while the sell command requires a product-name, sell-date and sell-price. Each of these arguments are tested seperately for being of the right type, ie. string, float, or date-object respectively. If an argument is missing or of the wrong type, an error message specific to the problem prompts the user enter it correctly.


**2. Testable code:**

SuperPy is written in such way that it's functions can easily be tested. For instance, instead of hardcoding file-paths into the functions, the paths are defined as global paramaters and then given as arguments to the function definition. These functions can then be tested with dummy or test-files.  
Take for example the ```buy_product``` function:  
```def buy_product(product_name, buy_date, buy_price, expiration_date, quantity, b_path=BOUGHT_PATH):```  
As the bought.csv file path is given as an argument to the function, one can choose to actualy provide another path to an example file when testing this function.   
In addition, all the function's print statements, which print the result of an CLI command, were moved out of the functions to the actual call-site. All SuperPy functions now only return a result, which are then printed at the call-site in main.py. These returns can easily be tested by Pytest, unlike a print statement.  
For instance:  The ```get_profit_day``` method in Ledger.py returns the profit over a specific day, which is then printed on the CLI by main.py. This profit return can be variefied with test files,  instead of having to test the ```get_profit_day``` function for it's side-effect of printing.

**3. The collection class Ledger**

Superpy contains the classes Product and Ledger. The class Ledger has a 'get_product' method which loads product data from the csv-files and creates a product instance for each bought product and updates it with information from the the sold-file. 

The collection class Ledger then loads all these Product instances into an instance list, or 'ledger'. Each time a user needs a report, such as profit or product-sales, class methods specific to the type of report requested can be invoked on an up-to-date ledger. 

The advantage of structuring the code in this way, is that the class ledger provides a data structure which is better geared towards generating reports, than extracting the specific data directly from the two 'bought' and 'sold' csv-files everytime a report is queried. Report parameters, such as type and date, can be adjusted easily on a ledger without having to rewrite any code. In addition, any new report-types that a user requires in the future (such as daily profit over a specific year) can easily be added as new 'get_report' methods within the ledger class. 




