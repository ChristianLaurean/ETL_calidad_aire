from airflow import DAG
from dag_default import DEFAULT_ARGS
from airflow.utils.dates import days_ago
from airflow.utils.task_group import TaskGroup
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.python_operator import PythonOperator
from air_quality.tasks import extract_location_and_air_quality, transform_data, load_data_into_redshift, send_air_quality_alerts




# Define DAG description
dag_description = """
    This DAG performs an ETL process for air quality data, including extraction, transformation, loading into Redshift, 
    and sending alerts if necessary.
"""



with DAG(
    dag_id="air_quality_pipeline",
    description=dag_description,
    default_args=DEFAULT_ARGS,
    start_date=days_ago(0),
    schedule_interval="0 22 * * *",# Every day at 10 PM
    max_active_runs=1,
    catchup=False,
    tags=["ETL", "air_quality"]
) as dag:
    



    # Add documentation to DAG
    dag.doc_md = """
        ### Air Quality Pipeline

        This DAG performs the ETL process for air quality data. It extracts location data and air quality data 
        from external APIs, transforms the data, loads it into a Redshift database, and sends alerts if necessary.
    """




    pre_workflow = DummyOperator(task_id="pre_workflow")

    with TaskGroup("etl", prefix_group_id=True) as pipeline:

        extract_task = PythonOperator(
            task_id="extract",
            python_callable=extract_location_and_air_quality
        )

        transform_task = PythonOperator(
            task_id="transform",
            python_callable=transform_data
        )

        load_task = PythonOperator(
            task_id="load",
            python_callable=load_data_into_redshift
        )

        extract_task >> transform_task >> load_task

    notification = PythonOperator(
        task_id="send_air_quality_alerts",
        python_callable=send_air_quality_alerts,
        provide_context=True
    )

    post_workflow = DummyOperator(task_id="post_workflow")

    pre_workflow >> pipeline >> notification >> post_workflow
