import snowflake.connector

source_account = 'wwwknga-br32220'
source_username = "89abhilash"
source_password = "89@Abhilash"
source_database = "FINANCEDWH"
source_warehouse = "COMPUTE_WH"
source_role = "ACCOUNTADMIN"
source_schema = "FDWH"

# Target Snowflake account credentials
target_account = 'nvalrcb-rh61158'
target_username = "SHUBHAM68"
target_password ="Shubham123"
target_database = "FINANCEDWH"
target_warehouse = "COMPUTE_WH"
target_role = "ACCOUNTADMIN"
target_schema = "FDWH"


# Establish connections to both source and target accounts
source_conn = snowflake.connector.connect(
    user=source_username,
    password=source_password,
    account=source_account,
    warehouse='COMPUTE_WH',  # Add your source warehouse name
    database=source_database,
    schema=source_schema
)

target_conn = snowflake.connector.connect(
    user=target_username,
    password=target_password,
    account=target_account,
    warehouse='COMPUTE_WH',  # Add your target warehouse name
    database=target_database,
    schema=target_schema
)


# Function to copy tables from source to targe


source_cursor = source_conn.cursor()
target_cursor = target_conn.cursor()
source_cursor.execute(f'SHOW TABLES IN SCHEMA {source_schema}')
table_rows = source_cursor.fetchall()

for row in table_rows:
    table_name = row[1] 
    # Fetch data from the source table
    select_query = f'SELECT * FROM {source_schema}.{table_name}'
    source_cursor.execute(select_query)
    rows = source_cursor.fetchall()
    print(rows)
    # Insert data into the target table
    insert_query = f'INSERT INTO {target_schema}.{table_name} VALUES ({", ".join(["%s"] * len(rows[0]))})'
    target_cursor.executemany(insert_query, rows)

    print(f'Data from {source_schema}.{table_name} has been inserted into {target_schema}.{table_name}.')

# Commit the transaction
target_conn.commit()

# Close connections
source_cursor.close()
target_cursor.close()
source_conn.close()
target_conn.close()

print('Data from all tables has been copied to the target schema.')
