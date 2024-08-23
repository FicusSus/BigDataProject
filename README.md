**Student Name**: Kira Solovjova
# COVID-19 Data Integration, Analysis, and Visualization Platform

## Technologies Used

### 1. **Snowflake**
   - **Purpose**: Snowflake is the primary data warehouse for structured COVID-19 data.
   - **Setup**: A free Snowflake trial account using AWS (Ohio region) is required. The platform uses Snowflake SQL to query datasets.
   - **Key Features**: 
     - Data warehousing for large-scale data analysis.
     - Query optimization and performance improvements with autocommit enabled.
     - Client session persistence to reduce reconnection overhead.

### 2. **Dash (by Plotly)**
   - **Purpose**: Provides the framework for building the web-based dashboard.
   - **Key Features**:
     - Interactive visualization with `dash_core_components` and `dash_html_components`.
     - Dropdowns, date pickers, and interactive charts for an enhanced user experience.

### 3. **Flask**
   - **Purpose**: Acts as the backend API server.
   - **Key Features**:
     - API endpoints for data retrieval.
     - Integration with Snowflake and MongoDB for fetching and inserting data.
     - Flask-CORS for handling cross-origin requests.

### 4. **MongoDB**
   - **Purpose**: Stores semi-structured data such as user comments.
   - **Setup**: The local MongoDB instance must be configured to accept connections.
   - **Key Features**:
     - Supports JSON-like document storage.
     - Provides flexible storage for non-relational data (e.g., user comments).

### 5. **Plotly and Matplotlib**
   - **Purpose**: These libraries generate visualizations for the dashboard.
   - **Key Features**:
     - Plotly for interactive and aesthetically rich visualizations.
     - Matplotlib for traditional static plots embedded in the dashboard.

### 6. **Dash-AG Grid**
   - **Purpose**: Displays tabular data in the dashboard with flexible features.
   - **Key Features**:
     - Responsive, customizable grids.
     - Can handle large datasets efficiently.

### 7. **Flask-Caching**
   - **Purpose**: Implements caching to improve performance.
   - **Key Features**:
     - Caches API responses to reduce database query load.
     - Supports configuration for various caching backends.

### 8. **Flask-CORS**
   - **Purpose**: Enables Cross-Origin Resource Sharing for API endpoints.
   - **Key Features**:
     - Ensures that API responses can be consumed by front-end applications hosted on different origins.

### 9. **pymongo**
   - **Purpose**: Python client for MongoDB to interact with the semi-structured data.
   - **Key Features**:
     - Efficient insertion and retrieval of JSON-like documents.

## Project Setup and Requirements

### Prerequisites

1. **Python 3.x**: The project is built in Python and requires Python 3.x to run. Install the latest version of Python from [python.org](https://www.python.org/downloads/).
2. **Snowflake Trial Account**:
   - Sign up for a free Snowflake trial [here](https://signup.snowflake.com/).
   - Ensure you select AWS as the cloud provider and use the Ohio region (us-east-2).
   - Configure your Snowflake account credentials in the `connect_snowflake` function.
3. **MongoDB**: Install and run a local MongoDB instance. You can download MongoDB from [mongodb.com](https://www.mongodb.com/try/download/community).

### Installation Steps

1. **Clone the Repository**:
   ```
   git clone <repo_url>
   cd covid19-data-platform
   ```

2. **Install Dependencies**:
   Install all required Python packages using `pip`:
   ```
   pip install -r requirements.txt
   ```
   The `requirements.txt` file should include the following:
   - `dash`
   - `flask`
   - `plotly`
   - `matplotlib`
   - `snowflake-connector-python`
   - `pymongo`
   - `flask-cors`
   - `flask-caching`
   - `dash-bootstrap-components`
   - `dash-ag-grid`
   - `requests`

3. **Configure Snowflake Credentials**:
   Update the `connect_snowflake` function in the `app.py` file with your Snowflake account details.

4. **Run MongoDB**:
   Ensure MongoDB is running locally:
   ```
   mongod --dbpath <your_db_path>
   ```

5. **Run the Backend Flask Server**:
   Start the Flask API server (this handles data fetching and caching):
   ```
   python app.py
   ```

6. **Run the Dash Application**:
   Start the Dash application to view the dashboard:
   ```
   python dashboard.py
   ```

7. **Access the Dashboard**:
   Visit `http://127.0.0.1:8050/` in your browser to explore the COVID-19 data visualization dashboard.

## Contribution Guidelines

1. **Branch Naming**: Use descriptive branch names (e.g., `feature-data-visualization`).
2. **Pull Requests**: Submit pull requests with clear descriptions of your changes.
3. **Testing**: Ensure that your code is tested before submitting. This includes both unit tests and functional tests where applicable.
4. **Code Reviews**: All code changes must go through a code review process before being merged into the main branch.


# Project Documentation: COVID-19 Data Integration Analysis and Visualization Platform

## Tasks and Implementation

### Task 1: Setup Snowflake and Fetch COVID-19 Data
The first step involved setting up the environment by creating a Snowflake trial account on the AWS Ohio region, as specified. Snowflake's free trial provides access to a wide range of datasets, including a COVID-19 dataset that contains global information on cases, vaccinations, and mortality rates.

*Implementation*:
- **Snowflake Trial Setup**: I registered for a Snowflake trial account and configured it to operate in the AWS Ohio region. This setup ensured compliance with the project’s guidelines and allowed me to leverage Snowflake’s features, such as scalable compute power and data sharing.
- **Data Importation**: I used Snowflake's Marketplace to locate and load the free COVID-19 dataset into a new database within Snowflake. This dataset included structured data on confirmed cases, recoveries, and deaths across different countries and regions.

### Task 2: Data Exploration and Enhancement
Once the data was in Snowflake, the focus shifted to exploring and enhancing the dataset. The goal was to uncover patterns in the data and identify any missing information that could improve our analysis. This required extensive use of SQL for data querying, cleaning, and preparation.

*Implementation*:
- **Data Exploration with SQL**: I began by writing SQL queries to inspect the structure of the COVID-19 dataset. This helped me understand the different tables, columns, and their relationships. Key queries focused on analyzing infection rates, death counts, and vaccination rates over time.
- **Data Gaps and Patterns**: Through SQL analysis, I identified trends, outliers, and any data gaps. For example, I noticed inconsistent data entries for specific regions during certain time periods, which led to decisions on data cleaning and preparation.

### Task 3: NoSQL Data Modeling in MongoDB
The platform required the ability to store user-generated data, such as comments or annotations on specific data points. This necessitated the use of a NoSQL database that could handle semi-structured data and scale flexibly. MongoDB was chosen for this task due to its document-oriented architecture, which is well-suited for storing varied and nested data structures.

*Implementation*:
- **MongoDB Setup**: I configured a MongoDB database to store supplementary data for the platform. MongoDB was chosen for its ability to handle flexible, schema-less documents, which is ideal for storing user annotations and comments.
- **Schema Design**: I designed a MongoDB schema that could accommodate user comments and annotations related to specific COVID-19 data points. The schema design was simple yet flexible, allowing for the storage of metadata such as user IDs, timestamps, and comment text.

### Task 4: API Development with Python
The project required an API to facilitate user interactions with the Snowflake and MongoDB databases. The API allows users to query COVID-19 data, submit comments, and retrieve annotations dynamically. Flask was selected for its simplicity and flexibility in building web APIs.

*Implementation*:
- **Flask Framework**: I built the API using Flask, which is a lightweight and easy-to-use framework for web development in Python. Flask was chosen for its simplicity in handling RESTful API requests and responses.
- **API Endpoints**: The API has multiple endpoints. Some of the core endpoints include:
    - **`/get_data`**: This endpoint queries Snowflake based on user inputs, such as a date range or region, and returns COVID-19 data.
    - **`/add_comment`**: This endpoint allows users to submit comments on specific data points, which are then stored in MongoDB.
    - **`/get_comments`**: This retrieves all user comments related to a specific data point from MongoDB.
- **Data Processing**: The API performs real-time data processing as required. For example, users may request summary statistics or specific views of the data, which are computed on-the-fly before being returned to the client.
- **Caching**: Flask-Caching was implemented to store frequently requested data, reducing the load on Snowflake and improving the API’s performance. Cached responses are stored temporarily to avoid redundant database queries for the same data.

### Task 5: Interactive Visualization with Python
The final task involved building a user-friendly visualization dashboard that could dynamically display the COVID-19 data. Dash and Plotly were used for the interactive components, while Matplotlib was utilized for static visualizations.

*Implementation*:
- **Dashboard Design**: I used Dash, a Python framework for building analytical web applications, to create an interactive dashboard. The dashboard allows users to select metrics (e.g., infection rates, mortality rates) and visualize the data in real time.
- **Visualization Features**: The visualizations are designed to be interactive and customizable. Users can select time periods to adjust the visual output. 
- **Chart Types**: Multiple types of charts were implemented:
    - **Line Charts**: For visualizing infection and mortality rates over time.
    - **Bar Charts**: To compare data across different regions or demographics.
    - **Static Visuals with Matplotlib**: In addition to interactive plots, some visualizations are rendered using Matplotlib for simpler static graphs that summarize key data points.

Each of these tasks was essential to the overall goal of the project, ensuring that the platform is both functional and capable of providing meaningful insights into the COVID-19 pandemic. The combination of structured data from Snowflake and semi-structured data from MongoDB, along with interactive visualizations, creates a powerful tool for understanding and exploring the impacts of the virus.

### Task 6: Analytical Features
I implemented advanced analytical features using both SQL-based data analysis and interactive visualizations. One of the key features I developed was clustering regions based on COVID-19 spread patterns. This allowed me to segment regions according to similarities in infection rates, enabling me to draw more granular insights into how the pandemic progressed.

*Implementation*:
- I used SQL queries in Snowflake to group data by geographical regions (e.g., country and state) and calculated metrics such as daily new cases and infection rates.
- In Python, I employed `plotly.express` to visualize these clusters in an interactive Dash dashboard, enabling users to filter and explore the data across different time frames.
- I also utilized libraries like `matplotlib` and `plotly` to generate both static and dynamic visualizations for comparative analysis.

### Task 7: Performance Optimization
To ensure efficient performance, I focused on optimizing my Snowflake SQL queries. By indexing frequently queried columns, using more specific SQL clauses instead of `SELECT *`, and applying proper partitioning, I reduced query execution times significantly. I also set up resource monitors in Snowflake to manage warehouse usage, preventing unnecessary costs while maintaining performance.

*Implementation*:
- I optimized Snowflake queries by carefully selecting only the necessary columns, avoiding inefficient `SELECT *` statements.
- I configured resource monitors in Snowflake to track and limit warehouse usage, helping to prevent over-provisioning and control query costs.
- I dynamically adjusted the size of the Snowflake warehouse to balance computational demand and ensure optimal performance during periods of high usage.

### Task 8: Caching for Frequently Requested Data
I implemented caching mechanisms within the Flask API to handle frequently requested data more efficiently. By using Flask-Caching, I stored the results of frequently accessed queries in memory, which reduced the load on the Snowflake warehouse and improved response times for repeated queries.

*Implementation*:
- I integrated `Flask-Caching` to cache API responses in memory, allowing me to reduce the number of redundant Snowflake queries.
- I set up caching based on the query string, ensuring that different query variations were cached separately for quicker retrieval in future requests.
- I configured the cache timeout to 300 seconds (5 minutes) to strike a balance between data freshness and performance.

### Task 9: Pattern Recognition
I utilized Snowflake’s `MATCH_RECOGNIZE` feature to identify patterns in the COVID-19 dataset. This allowed me to detect sequences of increasing or decreasing infection rates across different regions, providing valuable insights into the spread of the virus and helping me identify emerging trends such as infection waves.

*Implementation*:
- I created advanced SQL queries using `MATCH_RECOGNIZE` to detect patterns of consecutive daily increases in COVID-19 cases across various regions.
- By leveraging window functions, I was able to compare case numbers over successive days and highlight trends that indicated the onset of new infection waves.
- I exposed these patterns through API endpoints and visualized them on the dashboard, making it easier for users to identify regions with emerging trends.

*Example SQL Query*:
```sql
WITH case_comparison AS (
  SELECT 
    country_region,
    province_state,
    case_type,
    date,
    cases,
    LAG(cases, 1) OVER (PARTITION BY country_region, province_state, case_type ORDER BY date) AS previous_cases,
    LAG(cases, 2) OVER (PARTITION BY country_region, province_state, case_type ORDER BY date) AS two_days_ago_cases
  FROM JHU_COVID_19
  WHERE case_type = 'Confirmed'
)
SELECT country_region, province_state, date, cases
FROM case_comparison
WHERE cases > previous_cases AND previous_cases > two_days_ago_cases;
```
This query helped me identify consecutive increases in COVID-19 cases, revealing regions that were experiencing a surge.

## Conclusion
This project demonstrated my ability to integrate multiple technologies—Snowflake, Python, MongoDB, and Flask—to build a comprehensive and dynamic COVID-19 data analytics platform. By optimizing SQL queries, implementing caching mechanisms, and applying advanced pattern recognition techniques, I created an efficient tool for visualizing and analyzing pandemic data. The platform’s interactivity, combined with user annotations and comments, made it a valuable resource for extracting actionable insights from complex COVID-19 datasets.
