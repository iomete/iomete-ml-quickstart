import os
import time
from pyspark.sql import SparkSession
from pyspark.sql.functions import col
from pyspark.ml.feature import VectorAssembler
from pyspark.ml.regression import RandomForestRegressor
from pyspark.ml.evaluation import RegressionEvaluator
from pyspark.sql import SparkSession
from pyspark.sql import functions as F

start_time = time.time()

# MY_BUCKET = os.getenv("MY_BUCKET")
# MY_CSV_FILE = os.getenv("MY_CSV_FILE")


def generate_spark_data(spark, rows=10_000_000):
    print(f"Generating {rows} rows across the cluster...")

    # 1. Create an empty DataFrame with the desired number of rows
    # Spark distributes these rows across all workers immediately
    df = spark.range(0, rows)

    # 2. Use Spark SQL functions to generate random data in parallel
    df = df.withColumn("feature_col1", F.rand() * 100) \
           .withColumn("feature_col2", F.rand() * 100) \
           .withColumn("feature_col3", F.rand() * 100) \
           .withColumn("noise", F.randn() * 30)

    # 3. Apply your formula (y = 2x1 + 3x2^2 - sqrt(x3) + noise)
    # This calculation happens on the workers, not the driver!
    df = df.withColumn("target_col", 
        (F.col("feature_col1") * 2) + 
        (F.pow(F.col("feature_col2"), 2) * 3) - 
        (F.sqrt(F.col("feature_col3"))) + 
        F.col("noise")
    )

    # Drop the helper 'id' and 'noise' columns
    df = df.drop("id", "noise")
    return df


def main():
    spark = (
        SparkSession.builder
        .appName("RandomForestSparkExample")
        .getOrCreate()
    )

    # ---- READ OR GENERATE DATA ----
    # path = f"s3a://{MY_BUCKET}/{MY_CSV_FILE}"
    # df = spark.read.option("header", "true").option("inferSchema", "true").csv(path)
    print("Generating synthetic data...")
    df = generate_spark_data(spark)
    print("Data generation complete.")
    FEATURE_COLS = ["feature_col1", "feature_col2", "feature_col3"]
    MY_RESPONSE = "target_col"
    print(f"Initial rows: {df.count()}")

    print("Preparing features for ML...")
    # ---- PREPARE FEATURES ----
    assembler = VectorAssembler(
        inputCols=FEATURE_COLS, 
        outputCol="features"
        )
    
    df_ml = assembler \
        .transform(df) \
        .select(
            col("features"),
            col(MY_RESPONSE) \
                .alias("label")
        )
    
    # Repartition data for better parallelism
    df_ml = df_ml.repartition(120)

    # ---- TRAIN/TEST SPLIT (80-20) - Spark way ----
    print("Splitting data into Train and Test sets...")
    train_df, test_df = df_ml.randomSplit([0.8, 0.2], seed=42)
    print(f"Training rows: {train_df.count()} | Testing rows: {test_df.count()}")

    # ---- A RANDOM FOREST MODEL ----
    rf = RandomForestRegressor(
        featuresCol="features", 
        labelCol="label", 
        numTrees=100, 
        maxDepth=10
    )

    print("Training Random Forest on Cluster...")
    model = rf.fit(train_df)

    # ---- PREDICTIONS ----
    print("Generating predictions on Test set...")
    predictions = model.transform(test_df)
    predictions.select("prediction", "label", "features").show(5)

    # ---- EVALUATION METRICS ----
    print("Evaluating model performance...")
    evaluator_r2 = RegressionEvaluator(labelCol="label", predictionCol="prediction", metricName="r2")
    evaluator_rmse = RegressionEvaluator(labelCol="label", predictionCol="prediction", metricName="rmse")
    evaluator_mse = RegressionEvaluator(labelCol="label", predictionCol="prediction", metricName="mse")

    r2 = evaluator_r2.evaluate(predictions)
    rmse = evaluator_rmse.evaluate(predictions)
    mse = evaluator_mse.evaluate(predictions)

    print("\n" + "="*30)
    print("SPARK MODEL METRICS")
    print(f"R2 Score: {r2:.4f}")
    print(f"RMSE:     {rmse:.4f}")
    print(f"MSE:      {mse:.4f}")
    print("="*30 + "\n")

    spark.stop()

if __name__ == "__main__":
    main()

end_time = time.time()
print(f"Total time taken: {end_time - start_time:.2f} seconds")