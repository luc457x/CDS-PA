# Curry Company Growth Dashboard

This Growth Dashboard was built to track the growth metrics of Curry Company, a digital platform that connects Delivery Services and Restaurants.

## What this Growth Dashboard shows?
- **Company View**:
    - Tactical View: Weekly growth indicators.
    - Managerial View: General behavior metrics.
    - Geographical View: Geolocation insights.
- **Delivery Person View**:
    - Relevant metrics to track the performance of delivery services.
- **Restaurant View**:
    - Relevant metrics to track the performance of restaurants.

Deployed on: [Curry Company Growth Dashboard](https://currycomp.streamlit.app/) 

# Business Problems:

Curry Company is a marketplace that connects restaurants, delivery services, and customers. Trough the platform, restaurants can register their products and delivery services can register themselves to deliver the products from the restaurants to the customers.
The company generates many data about its operations and the management team is interested in viewing these data to understand the business performance. It should be organized in a dashboard that allows the team to see the results of the business and take data-driven decisions. The dashboard should be organized in 3 main views: Company, Delivery Services and Restaurants.
Further details and Key Business Questions can be found in the notebook of the project.

# Assumptions taken:

- The most important KPIs where number of orders, ratings and delivery time.
- The missing data could be handled discarting the rows with more than 2 missing values, the rest could be filled with meadian or mean values.
- Missing values in some columns such as "Festival","City" and "Road_traffic_density" could be filled with "Unknown", representating that the information was not provided.
- Since the company operates only in India, negative coordinates are considered misstyped and will be converted to positive. However, this should be taken with caution.
- Coordinates (0, 0), or "Null Islad", are considered valid and represents that the information was not provided or the GPS couldn't get a correct value, but distances are accurate. However, this should be taken with caution.
- The company does not have access to the unique IDs of delivery persons or cars; it only has access to the delivery services' unique IDs.

# Solution

## First step: Analysis
Using Python the data was cleaned and analyzed to answer the business questions. 
The tools used were: 
- Jupyter notebook to answer KBQs and document the process.
- Pandas to handle the data.
- Plotly and Folium to plot graphs.
## Second step: Dashboard
The dashboard was created using streamlit. It consists on 4 parts:
- Home: A brief introduction to the project.
- Company View: The main metrics for tactical and strategic decisions.
- Delivery View: Metrics about delivery services performance.
- Restaurant View: Metrics about restaurants performance.

# Top 3 insights

1. Gap in weekly order trend: There's a week in February with no orders, probably caused by a high occurrance of holidays and festivals.
2. Peak hours: The evening peak period, from 17:00 to 23:00, sees a significant surge in orders, far exceeding the morning peak between 08:00 and 11:00.
3. Restaurant density in Metro Areas: Metropolitan regions exhibit a higher concentration of restaurants, which correlates with elevated order volumes. However, this increased demand often coincides with traffic congestion.

# Final Product

- A notebook with answered KBQs and insights.<br>
The notebook can be found on the [Project's GitHub Repository](https://github.com/luc457x/CDS_PA-Curry_Company/blob/main/notebook.ipynb).
- A dashboard with the main metrics and graphs.<br>
The dashbord can be found on the [Streamlit Cloud](https://currycomp.streamlit.app/).

# Conclusion

The objective of this project was to create a dashboard to track the growth metrics of Curry Company, a digital platform that connects Delivery Services and Restaurants.
From the company view, we can see that the company is growing, with a increase in the number of orders, restaurants and delivery services.

# Next steps:

- Handle missing values better.
- Engenniring new features to improve metrics.
- Reduce the overall number of metrics on the dashboard.
- Create a predictive model to estimate delivery times and customer satisfaction.
