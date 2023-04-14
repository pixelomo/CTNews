from dotenv import load_dotenv
import os
import redis
import ssl

load_dotenv()
REDIS_URL = os.environ.get('REDIS_URL')

# Parse the URL to extract the different components
parsed_url = redis.Redis.from_url(REDIS_URL)

# Create a Redis connection using SSL
redis_conn = redis.Redis(
    ssl_cert_reqs=ssl.CERT_NONE,
)

# Test the connection
try:
    response = redis_conn.ping()
    print("Redis connected:", response)
except Exception as e:
    print("Error connecting to Redis:", e)
