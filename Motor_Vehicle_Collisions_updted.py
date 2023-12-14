from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import os
import pandas as pd

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2023, 1, 1),
    'email': ['admin@example.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'update_and_motor_vehicle_data',
    default_args=default_args,
    description='A DAG to update the fashion dataset and move it to a target directory in Codespace',
    schedule_interval=timedelta(days=1),
    catchup=False
)

def check_dataset_presence(dataset_path, dataset_filename):
    full_path = os.path.join(dataset_path, dataset_filename)
    if not os.path.exists(full_path):
        raise FileNotFoundError(f"The dataset {dataset_filename} was not found in {dataset_path}")
    return full_path

def update_dataset(full_path):
    df = pd.read_csv(full_path)
    # Perform any necessary modifications to df here
    # Example: Add a new column with static value "Updated"
    df['Updated'] = 'Yes'
    return df

def save_updated_dataset(df, target_path, dataset_filename):
    target_file_path = os.path.join(target_path, dataset_filename)
    # Ensure the target directory exists, create if it doesn't
    if not os.path.exists(target_path):
        os.makedirs(target_path)
    # Save the updated dataframe to the target directory
    df.to_csv(target_file_path, index=False)
    print(f"Updated dataset saved to {target_file_path}")

def update_and_motor_dataset(**kwargs):
    dataset_path = '/workspaces/hands-on-introduction-data-engineering-4395021'
    dataset_filename = 'Motor_Vehicle_Collisions.csv'
    target_path = '/workspaces/hands-on-introduction-data-engineering-4395021/Temporary'

    # Check dataset presence
    full_path = check_dataset_presence(dataset_path, dataset_filename)

    # Update dataset
    df = update_dataset(full_path)

    # Save updated dataset
    save_updated_dataset(df, target_path, dataset_filename)

update_and_move_dataset_task = PythonOperator(
    task_id='update_and_motor_vechicle_dataset',
    python_callable=update_and_motor_dataset,
    dag=dag,
)
