FROM iomete.azurecr.io/iomete/spark-py:3.5.5-latest

# switch to app directory
WORKDIR /app

# reset to root to run installation tasks
USER root

# ultra fast venv tool, uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# create a python virtual environment at /opt/venv
RUN uv venv /opt/venv

# update PATH so 'pip' and 'python' refer to the venv automatically
ENV PATH="/opt/venv/bin:$PATH"

# PYTHON for Spark executors
ENV PYSPARK_PYTHON="/opt/venv/bin/python" 

# PYTHON for Spark driver
ENV PYSPARK_DRIVER_PYTHON="/opt/venv/bin/python"

# install python dependencies into the venv using requirements.txt
COPY infra/requirements.txt ./
RUN uv pip install --python /opt/venv/bin/python -r requirements.txt

# Copy the application files
COPY job.py ./


# Specify the User that the actual main process will run as
ARG spark_uid=185
RUN chown -R ${spark_uid}:${spark_uid} /opt/venv
USER ${spark_uid}

