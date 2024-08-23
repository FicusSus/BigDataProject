# COVID-19 Data Integration, Analysis, and Visualization Platform

## Project Overview

The **COVID-19 Data Integration, Analysis, and Visualization Platform** is an interactive dashboard designed to analyze, visualize, and provide insights into the COVID-19 pandemic using diverse datasets hosted on Snowflake. This project integrates structured data (e.g., case numbers, vaccination stats) with semi-structured data (e.g., user comments), allowing for dynamic querying via an API, and visualizations through Plotly, Matplotlib, and Dash.

The platform was developed as part of a Data Engineering Bootcamp to demonstrate skills in backend development, data integration, and visualization. By connecting to Snowflake's COVID-19 dataset, the platform enables users to explore trends in confirmed cases, deaths, testing, and mobility data across different regions and periods.

## Features

- **Dynamic Data Visualizations**: Interactive bar charts generated with Plotly and Matplotlib.
- **Date Range Filtering**: Customizable date filters for querying specific time periods.
- **Caching for Performance**: Frequently requested data is cached to optimize performance.
- **APIs for Data Retrieval**: Flask APIs to fetch data from Snowflake and handle semi-structured MongoDB data.
- **Comment System**: Allows users to add comments tied to specific data points, stored in MongoDB.

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
