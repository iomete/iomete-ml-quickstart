# PySpark Machine Learning on IOMETE

This repository contains a production-ready template for distributed **Machine Learning training** using PySpark on the IOMETE Lakehouse.

Process is a spark job that you can deploy directly to IOMETE clusters. For more details on deploying spark jobs to IOMETE, refer to documentation [here](https://iomete.com/resources/developer-guide/spark-job/getting-started/).

Unlike the setup in the documentation above that uses `virtualenv`, this one uses a custom Docker environment powered by `uv` to ensure high-performance python libraries (like `numpy`, `pandas`) are pre-installed and optimized for the Spark 3.5.x runtime.

## 🧠 ML Capabilities

The included `job.py` provides a scalable **Linear Regression** pipeline that includes **Distributed Training**, i.e., training models across multiple Spark executors. It is purposefylly designed to be a starting point for more complex ML workflows. You can easily extend it to include:

* Feature Engineering (e.g., OneHotEncoding, Scaling)
* Different ML Algorithms (e.g., Decision Trees, Random Forests, XGBoost)
* Hyperparameter Tuning (e.g., Cross-Validation, Grid Search)

---

## 🛠 Tech Stack

* **Engine:** Apache Spark 3.5.x (PySpark)
* **Package Manager:** [uv](https://github.com/astral-sh/uv) (for 10x faster image builds)
* **Platform:** [IOMETE](https://iomete.com/)

---

## 📦 Environment Setup

### 1. Build Your ML Environment

This project bakes your code and dependencies into a Docker image so you don't have to install libraries at runtime.

```bash
# Clone and enter the repo
git clone https://github.com/iomete/iomete-ml-quickstart.git
cd iomete-ml-quickstart

# Build and push your custom ML image
# Make sure to update your registry path in the Makefile or .env
make docker-push

```

### 2. Prepare Your Data

Ensure your training data that is in an S3-compatible bucket is available in your IOMETE Lakehouse. 

---

## 🚀 Running the ML Job on IOMETE

It is just as any other Spark job on IOMETE. Follow the steps described in the [IOMETE Spark Job Documentation](https://iomete.com/resources/developer-guide/spark-job/getting-started/) to create and submit a new Spark job.

### Recommended Compute for ML

Training is memory-intensive but ofcourse distributed among multiple executors.

For this ML template, we recommend:

* **Driver:** 1 CPU / 4GB RAM (Handles the iterative coordination)
* **Executors:** 10+ Nodes (2 CPU / 8GB RAM each) to allow Spark to cache the training dataset in memory.

---

## 📂 Project Structure

| File | Description |
| --- | --- |
| **`job.py`** | **The ML Core.** Contains the SparkSession and model training logic. |
| `Dockerfile` | Uses `uv` to build a Python virtual env compatible with Spark. |
| `requirements.txt` | Define your libraries here. |
| `Makefile` | Utilities for building/pushing your Docker container. |

---

## 📈 Monitoring Training

Once the job is submitted:

1. Open the **Spark UI** from the IOMETE console.
2. Navigate to the **Stages** tab to monitor the progress of the distributed training iterations.
3. Check the **Logs** to view the training logs and any potential errors.

-- 

## Comparsion Results

To validate the performance of distributed training using PySpark on IOMETE, we compared the training time of a Linear Regression model on a synthetic dataset of 1 million rows and 1 feature, using both single-node and distributed training approaches.