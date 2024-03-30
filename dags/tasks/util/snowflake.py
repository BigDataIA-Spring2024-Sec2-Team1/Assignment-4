#!/usr/bin/env python
import warnings
import os

# from snowflake.sqlalchemy import

from sqlalchemy import create_engine

from dotenv import load_dotenv

load_dotenv()

warnings.filterwarnings("ignore")

SF_USERNAME = os.getenv("USERNAME")
SF_PASSWORD = os.getenv("PASSWORD")
SF_ACCOUNT_IDENTIFIER = os.getenv("ACCOUNT_IDENTIFIER")
DATABASE_NAME = os.getenv("DATABASE_NAME")
TABLE_NAME = os.getenv("TABLE_NAME")
WAREHOUSE_NAME = os.getenv("WAREHOUSE_NAME")
STAGE_NAME = os.getenv("STAGE_NAME")
STAGE_PATH = os.getenv("STAGE_PATH")

# current_folder_path = os.getcwd()


def get_engine():
    engine = create_engine(
        f"snowflake://{SF_USERNAME}:{SF_PASSWORD}@{SF_ACCOUNT_IDENTIFIER}/"
    )
    return engine


def create_database(engine):
    with engine.connect() as connection:
        result = connection.execute(f"SHOW DATABASES LIKE '{DATABASE_NAME}'")
        existing_databases = [row[1] for row in result.fetchall()]
        if DATABASE_NAME.upper() not in existing_databases:
            # Create database
            connection.execute(f"""CREATE OR REPLACE DATABASE {DATABASE_NAME};""")
            print(f"Database '{DATABASE_NAME}' created successfully.")
        else:
            print(
                f"Database '{DATABASE_NAME}' already exists. Skipping database creation."
            )
    engine.dispose()


def create_table(engine):
    with engine.connect() as connection:
        result = connection.execute(f"""SHOW TABLES LIKE '{TABLE_NAME}'""")
        existing_tables = [row[1] for row in result.fetchall()]
        print(existing_tables)
        # existing_databases = [row[1] for row in result.fetchall()]
        if TABLE_NAME.upper() not in existing_tables:
            # Create table
            connection.execute(f"""USE DATABASE {DATABASE_NAME};""")
            connection.execute(
                f"""CREATE OR REPLACE TABLE {TABLE_NAME} (
                text STRING,
                section_title STRING,
                file_path STRING,
                para STRING,
                paper_title STRING,
                year STRING,
                level STRING
                )"""
            )
            print("Table created successfully.")
        else:
            print("Table already exists. Skipping table creation.")
    engine.dispose()


def create_warehouse(engine):
    with engine.connect() as connection:
        result = connection.execute(f"SHOW WAREHOUSES LIKE '{WAREHOUSE_NAME}'")
        existing_warehouses = [row[0] for row in result]
        print(existing_warehouses)

        if WAREHOUSE_NAME.upper() not in existing_warehouses:
            # Create warehouse
            connection.execute(
                f"""CREATE OR REPLACE WAREHOUSE {WAREHOUSE_NAME} WITH
                WAREHOUSE_SIZE='X-SMALL'
                AUTO_SUSPEND = 180
                AUTO_RESUME = TRUE
                INITIALLY_SUSPENDED=TRUE;
                """
            )
            print(f"Warehouse '{WAREHOUSE_NAME}' created successfully.")
        else:
            print(
                f"Warehouse '{WAREHOUSE_NAME}' already exists. Skipping warehouse creation."
            )

    engine.dispose()


def create_stage(engine):
    with engine.connect() as connection:
        # Check if the stage exists
        result = connection.execute(f"SHOW STAGES LIKE '{STAGE_NAME}'")
        existing_stages = [row[1] for row in result]

        if STAGE_NAME.upper() not in existing_stages:
            # Create stage
            connection.execute(f"""USE DATABASE {DATABASE_NAME};""")
            connection.execute(
                f"""CREATE STAGE {STAGE_NAME} DIRECTORY = ( ENABLE = true );"""
            )
            print(f"Stage '{STAGE_NAME}' created successfully.")
        else:
            print(f"Stage '{STAGE_NAME}' already exists. Skipping stage creation.")

    engine.dispose()


def upload_files(engine, input_path):
    with engine.connect() as connection:
        # Upload files to stage
        connection.execute(f"""USE DATABASE {DATABASE_NAME};""")
        connection.execute(f"""PUT {input_path} @{STAGE_PATH};""")
    engine.dispose()


def copy_stage_to_table(engine, file_name):
    with engine.connect() as connection:
        # Copy stage to table
        connection.execute(f"""USE DATABASE {DATABASE_NAME}""")
        connection.execute(f"""USE WAREHOUSE {WAREHOUSE_NAME}""")
        connection.execute(
            f"""COPY INTO {TABLE_NAME}
          FROM @{STAGE_PATH}
          FILE_FORMAT = (type = csv field_optionally_enclosed_by='"')
          PATTERN = '.*metadata.csv.gz'
          ON_ERROR = 'skip_file';"""
        )
        print("hhhere")
    engine.dispose()

def view_table(engine):
    with engine.connect() as connection:
        connection.execute(f"""USE DATABASE {DATABASE_NAME};""")
        result = connection.execute(f"""SHOW TABLES LIKE '{TABLE_NAME}'""")
        existing_tables = [row[1] for row in result.fetchall()]
        print(existing_tables)
        if TABLE_NAME.upper()  in existing_tables:
            # Create table
            result = connection.execute(
                f"""SELECT * FROM {TABLE_NAME}"""
            )
            print("Data fetched successfully.")
            return result
        else:
            print("Table does not exists.")
            return None
    engine.dispose()


def push_data_to_snowflake(**kwargs):
    try:
        ti = kwargs['ti']
        input_path = ti.xcom_pull(key="output_file_path", task_ids="data_validation")
        # input_path = f'file:///opt/metadata.csv'
        engine = get_engine()
        create_database(engine)
        create_table(engine)
        create_warehouse(engine)
        create_stage(engine)
        upload_files(engine, input_path)
        copy_stage_to_table(engine, "metadata.csv")
        print("Done")
        return True
    except Exception as e:
        # Log the error message
        print(f"Error while uploading data to Snowflake: {e}")
        return False
