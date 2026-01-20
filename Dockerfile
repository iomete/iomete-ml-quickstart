FROM iomete.azurecr.io/iomete/spark-py:3.5.5-latest

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
COPY requirements.txt /tmp/requirements.txt
RUN uv pip install --python /opt/venv/bin/python -r /tmp/requirements.txt

# ensure the spark user owns the venv so it can execute scripts
RUN chown -R spark:spark /opt/venv

# switch to spark user
USER spark

# switch to app directory
WORKDIR /app