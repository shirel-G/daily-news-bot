# Airflow DAG: Daily Medium Articles

This Airflow DAG creates a directory and a file containing the latest Medium articles about Python, Golang, and Docker, respectively. The DAG runs once a day and uses only PythonOperator.

## Overview

The DAG consists of four tasks:

1. `create_directory`: creates a directory where the files will be stored, if it does not already exist.
2. `get_latest_medium_stories_python`: gets the latest 5 Medium articles about Python and saves them to a file.
3. `get_latest_medium_stories_golang`: gets the latest 5 Medium articles about Golang and saves them to a file.
4. `get_latest_medium_stories_docker`: gets the latest 5 Medium articles about Docker and saves them to a file.

Each task is implemented using a `PythonOperator`, which calls a Python function that performs the corresponding action. The `create_directory` task creates a directory at `/opt/airflow/dags/daily_medium_stories` if it does not already exist. The `get_latest_medium_stories` function gets the latest Medium articles about a given topic by querying the HackerNews API and saves them to a file in the same directory as the DAG.

## Usage

To use this DAG, save the code to a Python file and place it in your Airflow DAGs directory (`/opt/airflow/dags` by default). Then start the Airflow scheduler and webserver, and the DAG will be automatically loaded.

## Configuration

The following variables can be configured at the top of the DAG file:

* `DAGS_DIRECTORY`: the directory where the DAG file is located.
* `MEDIUM_STORIES_DIRECTORY`: the directory where the Medium articles will be stored.
* `default_args`: default arguments for the DAG, such as the owner and start date.
* `schedule_interval`: the frequency at which the DAG runs.
* `catchup`: whether or not Airflow should run any missed DAG runs upon starting.
* `get_latest_medium_stories`: the function that retrieves the latest Medium articles.

## Requirements

This DAG requires the following Python packages:

* `requests`: for making HTTP requests to the HackerNews API.
* `json`: for formatting the Medium article data.
* `datetime`: for generating the current date for the filename.
* `os`: for creating the directory and file.

## License

This code is licensed under the MIT License. See `LICENSE` for details.
