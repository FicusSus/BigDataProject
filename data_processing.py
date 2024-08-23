import snowflake.connector
import pymongo
from flask_cors import CORS
from datetime import datetime
from flask import Flask, request, jsonify, abort
from flask_caching import Cache  # Import Flask-Caching

app = Flask(__name__)
CORS(app)

# Setup Flask-Caching
cache = Cache(config={'CACHE_TYPE': 'SimpleCache', 'CACHE_DEFAULT_TIMEOUT': 300})  # In-memory caching
cache.init_app(app)

# Connection Pool for Snowflake
snowflake_pool = None

def connect_snowflake():
    global snowflake_pool
    if snowflake_pool is None:
        try:
            # Create a connection pool
            snowflake_pool = snowflake.connector.connect(
                user='FICUSSUS',
                password='Oksana776)',
                account='cm38812.us-east-2.aws',
                warehouse='DATA_APPS_DEMO',  # Adjust this warehouse size based on need
                database='COVID19_EPIDEMIOLOGICAL_DATA',
                schema='PUBLIC',
                autocommit=True,  # Enable autocommit to improve performance
                client_session_keep_alive=True  # Keep sessions alive to avoid reconnecting
            )
        except snowflake.connector.Error as e:
            print(f"Error connecting to Snowflake: {e}")
            abort(500, description="Error connecting to Snowflake")
    return snowflake_pool

def fetch_data_snowflake(query):
    conn = connect_snowflake()
    try:
        cursor = conn.cursor()
        # Ensure query is optimized, avoiding `SELECT *`
        cursor.execute(query)
        data = cursor.fetchall()
        columns = [desc[0] for desc in cursor.description]  # Get column names
        result = [dict(zip(columns, row)) for row in data]  # Convert rows to dictionaries
        return result
    except snowflake.connector.Error as e:
        print(f"Error executing query: {e}")
        abort(500, description="Error executing Snowflake query")
    finally:
        cursor.close()

# MongoDB connection for semi-structured data
def connect_mongodb():
    try:
        client = pymongo.MongoClient("mongodb://localhost:27017/")
        db = client['covid19_supplementary']
        return db
    except pymongo.errors.ConnectionError as e:
        print(f"Error connecting to MongoDB: {e}")
        abort(500, description="Error connecting to MongoDB")

def insert_comment(user_id, data_point_id, comment):
    db = connect_mongodb()
    try:
        comments_collection = db['user_comments']
        comments_collection.insert_one({
            'user_id': user_id,
            'data_point_id': data_point_id,
            'comment': comment,
            'timestamp': datetime.utcnow()
        })
    except pymongo.errors.PyMongoError as e:
        print(f"Error inserting comment: {e}")
        abort(500, description="Error inserting comment into MongoDB")

# Caching applied to frequently requested data
@app.route('/data', methods=['GET'])
@cache.cached(query_string=True)  # Cache the results based on the query string
def get_data():
    query = request.args.get('query')
    if not query:
        abort(400, description="Query parameter is required")
    try:
        data = fetch_data_snowflake(query)
        return jsonify(data)
    except Exception as e:
        print(f"Error in get_data: {e}")
        abort(500, description="Error fetching data")

@app.route('/comment', methods=['POST'])
def add_comment():
    data = request.json
    if not all(k in data for k in ('user_id', 'data_point_id', 'comment')):
        abort(400, description="Missing required fields: user_id, data_point_id, comment")
    user_id = data['user_id']
    data_point_id = data['data_point_id']
    comment = data['comment']
    try:
        insert_comment(user_id, data_point_id, comment)
        return jsonify({"message": "Comment added successfully"}), 201
    except Exception as e:
        print(f"Error in add_comment: {e}")
        abort(500, description="Error adding comment")

@app.route('/patterns', methods=['GET'])
def get_patterns():
    query = """
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
      WHERE case_type LIKE 'Confirmed'
    ),
    patterns AS (
      SELECT
        country_region,
        province_state,
        case_type,
        date AS start_date,
        LEAD(date) OVER (PARTITION BY country_region, province_state, case_type ORDER BY date) AS end_date,
        cases AS current_cases,
        previous_cases,
        two_days_ago_cases
      FROM case_comparison
      WHERE previous_cases IS NOT NULL
        AND two_days_ago_cases IS NOT NULL
        AND cases > previous_cases
        AND previous_cases > two_days_ago_cases
    )
    SELECT
      country_region,
      province_state,
      start_date,
      end_date,
      current_cases,
      previous_cases,
      two_days_ago_cases
    FROM patterns
    ORDER BY start_date DESC
    LIMIT 100;
    """
    try:
        data = fetch_data_snowflake(query)
        return jsonify(data)
    except Exception as e:
        print(f"Error in get_patterns: {e}")
        abort(500, description="Error fetching pattern data")


if __name__ == "__main__":
    app.run(debug=True, port=5000)
