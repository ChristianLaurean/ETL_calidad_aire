FROM apache/airflow:2.9.0

USER root

# Solucionar lo de psgo2
RUN apt-get update \
    && apt-get install -y \
        gcc \
        python3-dev \
        libpq-dev

USER airflow

COPY requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

#ENV PATH="/opt/airflow/src:/opt/airflow/dags:${PATH}"
ENV PYTHONPATH="/opt/airflow/src:/opt/airflow/dags:${PYTHONPATH}"


ENTRYPOINT [ "/usr/bin/dumb-init", "--", "/entrypoint" ]
CMD []