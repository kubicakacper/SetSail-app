# SetSail_app

I wanted to learn some Data Engineering stuff.

SetSail is an application responding to a real need of creating a live repository of yachts' charter offers.
Namely, there are thousands of companies offering their yachts for rent. Each of them having a website with yachts' description, specs and pricelists.
And there is a customer (let's say... Emily), who would like to choose the best offer (e.g. the cheapest 40-feet yacht from Split in Croatia in September).
What if she wouldn't need to search through all of these websites with different interface?
So, an idea came up to my mind, to create a website that would collect all necessary data and present it to Emily.
In the real world such an app requires a cooperation with the charter companies, but for my test application I use webscraping of few charter companies' websites.

It's an **ETL** app, where:
1) _Extract_ - webscraping using **Beautiful Soup**,
2) _Transform_ - preparing collected data to customer's analysis using **Pandas**,
3) _Load_ - transferring the data to **AWS RDS** db using **MySQL**.

ETL is going to be managed by **Airflow** to update the data hourly or daily (however I am currently struggling with an Airflow error, so it's a TODO thing).

Moreover, there is a search engine that queries, filters and sorts current data using **Spark 3.2**.
Therefore, Emily is able to quickly find the best charter offers from hundreds of thousands available.

The app is written and tested in **Python 3.10**

___

It's structure is the following.
In _**runnable**_ directory, there are:
- _pipeline.py_, which is a main function for the ETL
- _search_engine.py_ with a sample Spark search query

_**extract**_ directory consists of 2 scripts with data webscraping (one script for one website) and a simple script for csv reading.

In _**transform**_ folder there are 2 scripts that transform the data from those 2 websites to be compatible with the required schemas (that are defined in _schema.py_).
Further transformation is done in _mergeData.py_. _Calc.py_ is just a class I needed to use to calculations (it's not mine).

_**load**_ dir contains scripts that upload and manage the data to an online database (_loadToAWS_RDS.py_) and write a DataFrame to a csv file.

_**query**_ part has just a script that queries the relational database and saves Yachts table as a DataFrame.

_**airflow**_ is empty for now. Later, I want to automate the ETL using this tool.
