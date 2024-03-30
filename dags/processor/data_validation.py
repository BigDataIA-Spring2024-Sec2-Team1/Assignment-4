from tasks.clean import get_clean_csv

def validate_data(**kwargs):
    print("validating the data")
    try:
        is_valid = get_clean_csv()
        if is_valid:
            print("Validating data to complited successfully.")
        else:
            raise ValueError("Data is not valid")
    except Exception as e:
        print("in exception", e)