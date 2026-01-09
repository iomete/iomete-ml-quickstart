# PySpark Machine Learning on IOMETE

This repository provides a production-ready template for training Machine Learning models on the **IOMETE Lakehouse platform**. It features a high-performance Docker setup using `uv` for lightning-fast dependency management and `PySpark` for scalable linear regression.

## 🚀 Key Features

* **Optimized Build:** Uses `uv` for 10x faster Python package installation than standard `pip`.
* **Isolated Environment:** Implements a Python Virtual Environment (`venv`) to ensure compatibility with Spark 3.5.x and Python 3.12+.
* **IOMETE Integration:** Pre-configured to run seamlessly on IOMETE Spark clusters.

---

## 🛠 Prerequisites

Before you begin, ensure you have:

1. An active **IOMETE** account. 
2. **Docker** installed and authenticated to your container registry (e.g., ACR, Docker Hub).
3. `make` installed (optional, for using the Makefile).

---

## 📖 Getting Started

### 1. Setup Environment

Clone the repository and prepare your environment variables:

```bash
git clone <your-repo-url>
cd iomete-ml-quickstart
cp .env.example .env

```

*Edit `.env` to include your specific S3 bucket, file name and registry paths.*

### 2. Build and Push the Image

We use a custom Dockerfile that optimizes the Spark environment. Run the following command to build and push to your registry:

```bash
make docker-push
```

Here are the deployment steps, rewritten for clarity while strictly maintaining your original order for the configuration fields.

---

## 🚀 Deploying to IOMETE

Follow these steps to configure and launch your PySpark job on the IOMETE platform:

### 1. Access the Console

* Log in to your **IOMETE Console**.
* Navigate to the **Job Templates** section in the sidebar.
* Click on **New Job Template** to begin the setup.

### 2. Configure the Job Template

Fill in the template details in the following order:

1. **Name:** Give your job a unique name (e.g., `spark-ml-job`).
2. **Resource Bundle:** Select your preferred resource bundle from the dropdown.
3. **Namespace:** Choose the appropriate namespace for your environment.
4. **Job Type:** Select **Python** (ensure Java is not selected).
5. **Docker Image:** Enter the URI of the image you pushed (e.g., `your-registry.azurecr.io/spark-ml:latest`).
6. **Main Application File:** Set this to `local:///app/main.py`.
> **Note:** The `local:///` prefix is required as it points to the file already baked into your custom image.


7. **Compute:** Define your Driver/Executor CPU, Memory, and the number of nodes (e.g., 2 Executors).

### 3. Execution & Monitoring

* **Submit:** Click the submit button to initialize the job.
* **Monitor:** Open the job logs and/or Spark UI to view the training progress. 

---

## 📁 Repository Structure

* `main.py`: The PySpark ML training script.
* `Dockerfile`: Multi-stage build using `uv` and virtual environments.
* `requirements.txt`: Python dependencies (Numpy, Pandas, etc.).
* `Makefile`: Shortcuts for Docker operations.
