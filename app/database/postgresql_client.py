import os
import psycopg
from dotenv import load_dotenv

load_dotenv()

required_variables = [
    "POSTGRES_HOST",
"POSTGRES_PORT",
"POSTGRES_DB",
"POSTGRES_USER",
"POSTGRES_PASSWORD"
]

missing_variables = [
    value_name
    for value_name in required_variables
    if not os.getenv(value_name)
]

if missing_variables:
    raise ValueError( f"Missing PostgreSQL environment variables: {', '.join(missing_variables)}")

def get_postgresql_connection() -> psycopg.Connection :

    return psycopg.connect(host= os.getenv(required_variables[0]),
                           port = os.getenv(required_variables[1]),
                           dbname = os.getenv(required_variables[2]),
                           user = os.getenv(required_variables[3]), 
                           password = os.getenv(required_variables[4]))