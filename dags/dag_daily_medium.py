import requests
import json
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime, timedelta
import os

DAGS_DIRECTORY='/opt/airflow/dags'
MEDIUM_STORIES_DIRECTORY=f'{DAGS_DIRECTORY}/daily_medium_stories'

def get_latest_medium_stories(topic, file_path):
    # Search HackerNews for stories about the topic
    api_url = "https://hn.algolia.com/api/v1/search_by_date?query={}&tags=story&hitsPerPage=1000".format(topic)
    response = requests.get(api_url)
    stories = response.json()["hits"]

    medium_stories = []
    for story in stories:
        if story['url'] is not None and "medium.com" in story['url']:
            medium_stories.append({"title": story['title'], "link": story['url']})

    medium_stories = medium_stories[:5]
    pretty_stories = json.dumps(medium_stories, indent=4)

    print("Medium.com stories:")
    for story in medium_stories:
        print(story)

    now = datetime.now()
    date_str = now.strftime('%Y-%m-%d')
    filename = f'medium_digest_{topic}_{date_str}.txt'
    full_file_path=f'{file_path}/{filename}'

    with open(full_file_path, 'w') as f:
        f.write(pretty_stories)

def create_directory(directory_path):
    if not os.path.exists(directory_path):
        os.makedirs(directory_path)
        print('Directory created')
    else:
        print('Directory already exists')

default_args = {
    'owner': 'airflow',
    'start_date': datetime(2023, 3, 8),
    'retries': 1,
    'retry_delay': timedelta(minutes=5)
}

dag = DAG(
    'daily_medium_articles',
    default_args=default_args,
    schedule_interval=timedelta(days=1),
    catchup=False
)

create_directory_task = PythonOperator(
    task_id='create_directory',
    python_callable=create_directory,
    op_kwargs={'directory_path': MEDIUM_STORIES_DIRECTORY},
    dag=dag
)

create_python_daily_medium_file_task = PythonOperator(
    task_id='get_latest_medium_stories_python',
    python_callable=get_latest_medium_stories,
    op_kwargs={'topic': 'python', 'file_path': MEDIUM_STORIES_DIRECTORY},
    dag=dag
)

create_golang_daily_medium_file_task = PythonOperator(
    task_id='get_latest_medium_stories_golang',
    python_callable=get_latest_medium_stories,
    op_kwargs={'topic': 'golang', 'file_path': MEDIUM_STORIES_DIRECTORY},
    dag=dag
)

create_docker_daily_medium_file_task = PythonOperator(
    task_id='get_latest_medium_stories_docker',
    python_callable=get_latest_medium_stories,
    op_kwargs={'topic': 'docker', 'file_path': MEDIUM_STORIES_DIRECTORY},
    dag=dag
)

create_directory_task >> [create_python_daily_medium_file_task, create_golang_daily_medium_file_task, create_docker_daily_medium_file_task]