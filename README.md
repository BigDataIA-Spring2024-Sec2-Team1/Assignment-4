# Assignment-4


# How to run the application


`Make sure you have docker upend running with atleast 4GB of memory`


`Step 1` -> `docker-compose up airflow-init`


`Step 2` -> `docker-compose up`


## DBT Code is in Below Branch
https://github.com/BigDataIA-Spring2024-Sec2-Team1/Assignment-3/tree/Aniketgiram-patch-1
    
## Links
Codelab: https://codelabs-preview.appspot.com/?file_id=1bOLtJd9YLoInM7W4p1JACNyj-XZh1Pkn0eEy6gx4R6U/edit?usp=sharing#0


## Project Structure TO BE UPDATED
```
.
├── Dockerfile
├── README.md
├── backend
│   ├── Dockerfile
│   ├── __pycache__
│   │   └── main.cpython-39.pyc
│   ├── main.py
│   └── requirements.txt
├── config
├── dags
│   ├── __pycache__
│   │   └── workflow.cpython-312.pyc
│   ├── processor
│   │   ├── __pycache__
│   │   │   ├── data_validation.cpython-312.pyc
│   │   │   ├── grobid_parse.cpython-312.pyc
│   │   │   ├── init_setup.cpython-312.pyc
│   │   │   └── upload_to_snowflake.cpython-312.pyc
│   │   ├── data_validation.py
│   │   ├── grobid_parse.py
│   │   ├── init_setup.py
│   │   ├── read_data.py
│   │   └── upload_to_snowflake.py
│   ├── tasks
│   │   ├── __init__.py
│   │   ├── __pycache__
│   │   │   ├── __init__.cpython-312.pyc
│   │   │   └── clean.cpython-312.pyc
│   │   ├── clean.py
│   │   └── util
│   │       ├── __init__.py
│   │       ├── __pycache__
│   │       │   ├── __init__.cpython-312.pyc
│   │       │   └── snowflake.cpython-312.pyc
│   │       ├── pydantic_models
│   │       │   ├── __init__.py
│   │       │   ├── __pycache__
│   │       │   │   ├── __init__.cpython-312.pyc
│   │       │   │   └── pydantic_classes.cpython-312.pyc
│   │       │   └── pydantic_classes.py
│   │       └── snowflake.py
│   └── workflow.py
├── docker-compose.yaml
├── frontend
│   ├── Dockerfile
│   └── main.py
│   └── scheduler
│       ├── 2024-03-30
│       │   └── workflow.py.log
│       └── latest -> 2024-03-30
├── plugins
└── requirements.txt
```



## Team Information and Contribution 

Name | Contribution %| Contributions |
--- |--- | --- |
Aniket Giram    | 45% |Part 1 |
Sudarshan Dudhe | 40% |Part 2 |
Rasika Kole     | 15% |Documentation |
