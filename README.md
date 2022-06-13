# SetSail_app
SetSail ETL app - under consctruction

Since November 2021 I am learning to become a Data Engineer.
This is gonna be the first project to my portfolio.

SetSail is an application responding to a real need of creating a live repository of yachts' charter offers.
Namely, there are thousands of companies offering their yachts for rent. Each of them having a website with yachts' description, specs and pricelists.
And there is a customer (let's say... Emily), who would like to choose the best offer (e.g. the cheapest 40-feet yacht from Split in Croatia in September).
What if she wouldn't need to search through all of these websites with different interface?
So, an idea came up to my mind, to create a website that would collect all necessary data and present it to Emily.
In the real world such an app requires a cooperation with the charter companies, but for my test application I use webscraping of few charter companies' websites.

It's an **ETL** app, where:
1) Extract - webscraping using **Beautiful Soup**
2) Transform - preaparing collected data to customer's analysis using **Pandas** and **Spark 3.2**
3) Load - transferring the data to **AWS RDS** db using **MySQL**, so it can be used in a future live repository published to WWW

and all managed by **Airflow** to update the data hourly or daily


That's the plan, let's get back to work.
