# SuperPy User Guide

## SuperPy Description

SuperPy is a python Command Line Interface (CLI) program that enables users to keep track of a supermarket inventory and report on income data.

With command line arguments a user can::
- log products as bought or sold in an inventory, 
- retrieve information on products based on product ID, 
- report on profit, revenue or product sales over time, 
- and set, view and change the date that the program views as 'today'

SuperPy uses csv-files to keep track of product sales, and python classes to create ledgers and reports on profit and revenue over time. Report plots will show directly on the CLI but can be exported as tables to excel files, or as figures to PDF and JPEG images.

The following modules need to be installed in order to run SuperPy:

- Python (3.7.3)
- Matplotlib (3.5.1)
- pandas (1.3.4)
- Tabulate (0.8.9)




## SuperPy commands

The SuperPy program consists of the following sub-commands:
        
    buy /sell / show-product / show-inventory / report-total / report-overtime /
    show-date / set-date / change-date

Each of these sub-commands in turn requires it's own arguments and flags. While most potional and named arguments are required, some are optional and have default values set. The arguments for each sub-command are checked for type so users are promted to enter date and vales in the correct format.



To start SuperPy, open the superpy folder in the CLI and type the command:

```./superpy> python main.py ```

followed by one of the sub-commands.

Each sub-command is explained below, and examples are provided. 

&nbsp;


## The DATE commands

SuperPy keeps track of date.  The date that this program views as 'today', is stored internally in a csv-file as the variable 'today'.  This date can be viewed, set and moved forward or backwards by the user with the following commands: 

```$ show-date```  
*Shows the date that SuperPy has stored as 'today'.*  
```$ set-date <date>```  
*Sets date to input date, enter in format YYYY-MM-DD.*  
```$ change-date <number of days>```  
*Advances the date a specific number of days, entered as an integer. Date can also be moved backward by entering a negative integer.*  

Only the very first time the SuperPy program is used by a user, the today variable is set automatically to the current date. After this,  the today variable has to be changed by the user with ```set-date``` or ```change-date``` before logging products as bought/sold or when otherwise using the 'today' value on the command-line.


### Examples of DATE commands
```
$ python main.py show-date  
This program has today's date stored as 2021-31-1
```
```
$ python main.py set-date 2022-01-17
This program has today's date stored as 2022-01-17
```
```
$ python main.py change-date 2
This program's date has been changed to 2021-01-19
```
```
$python main.py change-date -2
This program's date has been changed to 2021-01-17
```

&nbsp;

## The BUY command: logging products as bought

With the 'buy' command a user can log a product into the inventory.  The buy-command is followed by named-arguments to store product information. These arguments are either required or set to default so that the inventory does not contain missing data-fields

The following named-argumentss are required:  
```--product <product-name>```   
*Name of the bought product.*  
```--price <price>```   
*Price of the product entered as float with one decimal.*    
```--expiration <expiration>```  
*Expiration date in format 'YYYY-MM-DD'.*

The following named-arguments are optional:  
```--quantity <product quantity>```  
*The number of products bought on the same date, for the same price and with a similar expiration date. Default  is 1.*    
```--buydate <buy-date>```  
*Enter 'today', 'yesterday' or date in format 'YYYY-MM-DD'. Default is 'today'.*  

When an user logs product for the first time a csv-file 'bought.csv' will be created in the SuperPy folder. Afterwards, anytime a user logs products as bought, these products will be added to this file. Products get assigned a 'biught_id' based on the order they are added to the csv-file.

The default buy-date for logging a product as bought is the date stored as 'today'. This date can be set or changed by the user with the ```set-date``` or ```change-date``` sub-commands. There are two ways  a user can log products bought in the past (in case of back-log), thus before the 'today' date. 
1. Use the optional ```--buydate``` argument to enter this specific date. For example, if today's date is 2022-01-01, someone can enter backlogged product data by entering  ```--buydate 2021-12-1``` after the buy command. 
2. Set or change the program's 'today' variable to that past date. This will be especially useful when having to log a large number of products as bought on a certain date in the past, as the user then can omit the `--buydate` argument and which will be set to it's default 'today'.  


### Examples of BUY:  


Loggin a product as bought for the very first time:
```
$ python main.py buy --product apple --price 1.4 --expiration 2022-03-01 --buydate 2022-01-10
Created bought.csv
Logged apple in 'bought.csv' with product_id 1
```
Logging multiple products at once: 
```
$ python main.py buy --product banana --price 0.8 --expiration 2022-03-15 --buydate 2022-01-12 --quantity 3
Logged banana in 'bought.csv' with product_id 2
Logged banana in 'bought.csv' with product_id 3
Logged banana in 'bought.csv' with product_id 4
```

Changing the 'today' date and logging products without entering a buy-date:
```
$ python main.py show-date 
This program has today's date stored as 2022-01-17
$ python main.py set-date 2022-01-15
This program's date has been set to 2022-01-15
$ python main.py buy --product mango --price 2 --expiration 2022-04-01
Today's date is set to  2022-01-15
Logged mango in 'bought.csv' with product_id 5
```


The above commands store the example data to bought.csv as follows:

![Example of bought.csv](./userguide_images/example_boughtcsv.jpg)

&nbsp;


## The SELL command: logging products as sold

With the 'sell' command a user can log a product from the inventory as sold.  The sell-command is followed by named-arguments to store product information. These arguments are either required or set to default so the inventory does not contain missing data-fields. 

The following named-arguments are required:  
```--product <product-name>```  
*Name of the sold product*   
```--price <sell-price>```  
*Price for which the product was sold entered as float with one decimal.* 

The following named-arguments are optional:  
```--quantity <product quantity>```  
*Number of products sold on the same date, for the same price. Optional argument, default is 1.*   
```--selldate <sell-date>```   
*Enter 'today', 'yesterday' or date in format 'YYYY-MM-DD'. Default is 'today'.*  
 

When an user logs products as sold for the first time, a csv file sold.csv will be created in the SuperPy folder. Afterwards, anytime a user logs products as sold, these products will be added to this file. The program assigns a sold product a new (sold-)id, and links this to the bought-id of the product.

The default sell-date for logging a product as sold, is the date stored as 'today'. This date can be set or changed with the `set-date` or `change-date` sub-command. If a user needs to enter a product which was sold in the past (before 'today'), the `--selldate` argument can be used to enter this specific date. Alternatively, the user can set or change the program's 'today' variable to that specific date. This will be especially useful when having to log a large number of products  on a certain date as sold, as the user can then omit the `--selldate` argument which wil be set to it's default 'today'.  

### Examples of SELL:

Loggin a product as sold for the very first time:
```
$ python main.py sell --product apple --price 2.0 --selldate 2022-01-12
Created sold.csv
Added apple to 'sold.csv' with sold-id 1 and bought-id 1
```
Logging multiple products as sold at once: 
```
$ python main.py sell --product banana --price 1.5 --selldate 2022-01-14 --quantity 2
Added banana to 'sold.csv' with sold-id 2 and bought-id 2
Added banana to 'sold.csv' with sold-id 3 and bought-id 3
```

Changing 'today' and logging products without entering a selldate:
```
$ python main.py show-date 
This program has today's date stored as 2022-01-17
$ python main.py change-date 2
This program's date has been changed to 2022-01-19
$ python main.py sell --product mango --price 3
Today's date is set to 2022-01-19
Added mango to 'sold.csv' with sold-id 4 and bought-id 5
```

Trying to sell a multiple products of which one is not in stock:
```
$ python main.py sell --product banana --price 1.5 --selldate 2022-01-15 --quantity 2
Added banana to 'sold.csv' with sold-id 5 and bought-id 4
Error: remaining product(s) not in stock
```

The above commands store the example data to sold.csv as follows:

![Example of sold.csv](./userguide_images/example_soldcsv.jpg)


&nbsp;

## The SHOW-PRODUCT command: 
## Retrieving product info

With the show-product subcommand a user can retrieve information on the buy, sell and expiry data of a product, given the product id.

The show-product command is followed by only one positional argument:

```product-id```  
*The ID assigned to the product when it was logged as bought (ie. bought id). Entered as integer, required.* 

### Examples of SHOW-PRODUCT

Showing data on a sold product:
```
$ python main.py show-product 4

 Product ID: 4
 Product bought on: 2022-01-12
 Product expires on: 2022-03-15

 Product sold on: 2022-01-15
 Product sold for: $1.5
 Product sold for: $1.5

```

Showing data on an expired (not sold) product:
```
$ python main.py set-date 2022-07-01
This program's date has been set to 2022-07-01
$ python main.py show-product 8

 Product ID: 8
 Product name: apple
 Product bought on: 2022-01-20
 Product bought for: $0.5
 Product expires on: 2022-04-01

PRODUCT EXPIRED
```

&nbsp;

## The SHOW-INVENTORY command: show the inventory on a specific day

The show-inventory command reports on the inventory on a specific day. It is followed by the required positional argument 'date'. The inventory is then shown in the CLI in a table. The data can be exported to a csv or excel-file, by using the optional flags. 

Required positional argument:  
```inventory-date```  
*The inventory date given as 'today', 'yesterday' or as date in format YYYY-MM-DD. Default is 'today'*

Flags (optional arguments):  
```--to-csv```  
*When this flag is entered the inventory is saved as a csv-file in the folder superpy/reports*  
```--to-excel```  
*When this flag is entered the inventory is saved as an excel-file in the folder superpy/reports*  
 
The inventory will only shows products which were already bought before the input date and which have not been sold or only sold after the input date. The inventory does not include expired products. 


## Examples of SHOW-PRODUCT

Show inventory on 13th of January 2022:
```
$ python main.py show-inventory 2022-01-13
+------+-----------+------------+-------------+--------------+
|   id | product   | buy_date   |   buy_price | expiration   |
|------+-----------+------------+-------------+--------------|
|    2 | banana    | 2022-01-12 |         0.8 | 2022-03-15   |
|    3 | banana    | 2022-01-12 |         0.8 | 2022-03-15   |
|    4 | banana    | 2022-01-12 |         0.8 | 2022-03-15   |
+------+-----------+------------+-------------+--------------+
```

Show inventory and save data both as excel spreadsheet and csv-file:

```
$ python main.py show-inventory 2022-01-16 --to-excel --to-csv
+------+-----------+------------+-------------+--------------+
|   id | product   | buy_date   |   buy_price | expiration   |
|------+-----------+------------+-------------+--------------|
|    5 | mango     | 2022-01-15 |           2 | 2022-04-01   |
+------+-----------+------------+-------------+--------------+
Inventory saved as 'Inventory on 2022-01-16.csv' in Superpy/reports folder
Inventory saved as 'Inventory on 2022-01-16.xlsx' in Superpy/reports folder
```

&nbsp;


## The REPORT-TOTAL command: 
## reporting on total profit and revenue 


The 'report-total' commands returns total revenue or profit for a given day, month or year.
The report-total command is followed by the required positional argument 'report-type', which can be either profit or revenue. Subsequently, the reporting period needs to be set with one of the named-arguments --day, --month or --year:

Required positional argument:  
```type-of-report```  
*The type of report the user wants to obtain. Choices are "revenue" or "profit".*  

Named arguments, choose one of three:  
```--day```  
*Returns revenue or profit for a given date. Date can be entered as 'today', 'yesterday' or as format YYYY-MM-DD.*  
```--month```   
*Returns revenue or profit for a given month. Enter in format YYYY-MM*  
```--year```  
*Returns revenue or profit for a given year. Enter in format YYYY*  


    

## Examples of REPORT-TOTAL

```
$ python main.py report-total revenue --day 2022-01-12
Total revenue on 2022-01-12: 2.0
```
```
$ python main.py report-total revenue --year 2022      
Total revenue in 2022: 9.5
```

```
$ python main.py report-total profit --day 2022-01-12  
Total profit on 2022-01-12: -0.4
```
```
$ python main.py report-total profit --month 2022-01
Total profit in January 2022: 1.2
``` 

&nbsp;

## The REPORT-PERIOD command: 
## reporting revenue, profit or sales over time.

With the report-period command a user can plot daily revenue, profit or product-sales over a given month. This subcommand is followed with the two positional arguments 'month' and 'report-type'. The 'report-type' can be set to 'revenue', 'profit', 'revenue-profit' (to show both in the same plot), or product-sales. The latter returns the number of sold items per day over a given month, for a specific product . When 'report-type' is set to 'product-sales', it should be followed with the named-argument '--product' and the product name for which the user wants to see sales. The data of all report-types can be saved as a csv-file or an excel-spreadsheet, and the plots can be exported to JPEG or PDF with the following flags '--to-csv', '--to-excel', '--to-jpeg' and '--to-pdf'.


Required positional arguments:  
```report-month```  
*The month for which daily revenue, profit or product-sales data will be calculated. 
Enter in format YYYY-MM*  
```report-type```  
*The type of report, choices are 'revenue', 'profit', 'revenue-profit' (showing both), or 'product-sales'*


Named-arguments:  
```--product```   
*The name of the product for which sales will be reported. 
This argument is only required when report-type is set to 'product-sales'.*  


Flags:  
```--to-csv```  
*Saves plot data in csv file.*  
```--to-excel```  
*Saves plot data as table in as Excel spreadsheet.*  
```--to-pdf```  
*Saves plot figure as PDF.*  
```--to-jpeg```  
*Saves plot figure as JPEG image.*

### Examples of REPORT-PERIOD

Reporting revenue for January 2022 and saving data in an Excel-spreadsheet.

```
$ python main.py report-period 2022-01 profit --to-excel
+-------+----------+
|   Day |   Profit |
|-------+----------|
|     1 |      0   |
|     2 |      0   |
|     3 |      0   |
|     4 |      0   |
|     5 |      0   |
|     6 |      0   |
|     7 |      0   |
|     8 |      0   |
|     9 |      0   |
|    10 |     -1.4 |
|    11 |      0   |
|    12 |     -0.4 |
|    13 |      0   |
|    14 |      3   |
|    15 |     -0.5 |
|    16 |      0   |
|    17 |      0   |
|    18 |      0   |
|    19 |      3   |
|    20 |     -2.5 |
|    21 |      0   |
|    22 |      0   |
|    23 |      0   |
|    24 |      0   |
|    25 |      0   |
|    26 |      0   |
|    27 |      0   |
|    28 |      0   |
|    29 |      0   |
|    30 |      0   |
|    31 |      0   |
+-------+----------+
Table saved as 'profit for January 2022.xlsx' in Superpy/reports folder
```

The plot will be shown as a Matplotlib figure, which needs to be closed before a user can use the CLI again. 

![Example of profit plot](./userguide_images/example_profit_plot.jpg)

Plotting the daily sales of apples over Januray 2022 and saving the figure as PDF:
```
$ python main.py report-period 2022-01 product-sales --product apple --to-pdf
+-------+-------------------------+
|   Day |   Number of apples sold |
|-------+-------------------------|
|     1 |                       0 |
|     2 |                       0 |
|     3 |                       0 |
|     4 |                       0 |
|     5 |                       0 |
|     6 |                       0 |
|     7 |                       0 |
|     8 |                       0 |
|     9 |                       0 |
|    10 |                       0 |
|    11 |                       0 |
|    12 |                       1 |
|    13 |                       0 |
|    14 |                       0 |
|    15 |                       0 |
|    16 |                       0 |
|    17 |                       0 |
|    18 |                       0 |
|    19 |                       0 |
|    20 |                       0 |
|    21 |                       0 |
|    22 |                       2 |
|    23 |                       1 |
|    24 |                       1 |
|    25 |                       1 |
|    26 |                       0 |
|    27 |                       0 |
|    28 |                       0 |
|    29 |                       0 |
|    30 |                       0 |
|    31 |                       0 |
+-------+-------------------------+
Figure saved as 'product-sales for January 2022.pdf' in Superpy/reports folder
```
The plot will look as follows:

![Example of product sales plot](./userguide_images/example_product_sales_plot.jpg)



