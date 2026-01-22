FROM iomete.azurecr.io/iomete/spark-py:3.5.5-latest

# switch to app directory
WORKDIR /app

# reset to root to run installation tasks
USER 0

# add requirements.txt first to leverage Docker cache
COPY infra/requirements.txt ./
RUN pip install --no-cache-dir --break-system-packages -r requirements.txt

# Copy the application files
COPY job.py ./

# Specify the User that the actual main process will run as
ARG spark_uid=185
USER ${spark_uid}
