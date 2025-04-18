from sqlite3 import connect
from pathlib import Path
from functools import wraps
import pandas as pd

# Using pathlib, create a `db_path` variable
# that points to the absolute path for the `employee_events.db` file
db_path = Path(__file__).resolve().parent / 'employee_events.db'


# OPTION 1: MIXIN
# Define a class called `QueryMixin`
class QueryMixin:
    
    # Define a method named `pandas_query`
    # that receives an sql query as a string
    # and returns the query's result
    # as a pandas dataframe
    def pandas_query(self, sql_query, params=None):
        connection = None
        try:
            connection = connect(db_path)
            if params:
                result = pd.read_sql_query(sql_query, connection, params=params)
            else:
                result = pd.read_sql_query(sql_query, connection)
            return result
        finally:
            if connection:
                connection.close()
        

    # Define a method named `query`
    # that receives an sql_query as a string
    # and returns the query's result as
    # a list of tuples. (You will need
    # to use an sqlite3 cursor)
    def query(self, sql_query, params=None):
        connection = None
        try:
            connection = connect(db_path)
            cursor = connection.cursor()
            if params:
                result = cursor.execute(sql_query, params).fetchall()
            else:
                result = cursor.execute(sql_query).fetchall()
            return result
        finally:
            if connection:
                connection.close()
    
 # Leave this code unchanged
def query(func):
    """
    Decorator that runs a standard sql execution
    and returns a list of tuples
    """

    @wraps(func)
    def run_query(*args, **kwargs):
        query_string = func(*args, **kwargs)
        connection = connect(db_path)
        cursor = connection.cursor()
        result = cursor.execute(query_string).fetchall()
        connection.close()
        return result
    
    return run_query
