import pandas as pd
from connection import engine
from models import Base

# List of table names
table_names = ['hubs', 'channels', 'drivers', 'stores', 'orders', 'payments', 'deliveries']

def correct_datetime_columns(df):
    """
    Dynamically converts all date/time columns to the correct PostgreSQL format (YYYY-MM-DD HH:MM:SS).
    
    Parameters:
        df (pandas.DataFrame): The DataFrame containing the data to be corrected.
    
    Returns:
        pandas.DataFrame: The DataFrame with corrected date/time columns.
    """
    # Iterate through the DataFrame columns
    for column in df.columns:
        # Check for columns related to date/time (those containing "moment" in the name)
        if 'moment' in column.lower():
            # Convert the column to datetime with the specified format
            df[column] = pd.to_datetime(df[column], format='%m/%d/%Y %I:%M:%S %p')
    
    return df

# Drop existing tables and create new ones based on the models defined in 'Base'
Base.metadata.drop_all(engine, checkfirst=True)
Base.metadata.create_all(engine)

# Load and insert data into each table
for table_name in table_names:
    # Read data from the corresponding CSV file
    df = pd.read_csv(f'data/{table_name}.csv', encoding='latin-1')

    # Correct datetime columns for 'orders' table
    if table_name == 'orders':
        df = correct_datetime_columns(df)

    # Insert data into the respective table in the database
    df.to_sql(table_name, con=engine, schema='public', if_exists='append', index=False)