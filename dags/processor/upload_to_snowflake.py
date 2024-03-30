from tasks.util.snowflake import push_data_to_snowflake

def upload_to_snowflake(**kwargs):
    print("Upload the data to snowflake.")
    try:
        is_valid = push_data_to_snowflake(kwargs=kwargs)

        if is_valid:
            # Implement your Snowflake upload logic here
            print("Uploading data to Snowflake")
        else:
            raise ValueError("Uploading data to Snowflake failed")
    except Exception as e:
        print("in exception", e)
