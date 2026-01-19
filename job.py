from pyspark.sql import SparkSession
from pyspark.sql.functions import col
from pyspark.ml.feature import VectorAssembler
from pyspark.ml.regression import LinearRegression
from dotenv import load_dotenv
import os

load_dotenv()

MY_BUCKET = os.getenv("MY_BUCKET")
MY_CSV_FILE = os.getenv("MY_CSV_FILE")
MY_SINGLE_NUMERIC_FEATURE = os.getenv("MY_SINGLE_NUMERIC_FEATURE")
MY_RESPONSE = os.getenv("MY_RESPONSE")

def main():
    spark = (
        SparkSession.builder
        .appName("LinearRegressionExample")
        .getOrCreate()
    )

    # ---- READ DATA FROM S3 COMPATIBLE STORAGE (DISTRIBUTED) ----
    df = (
        spark.read
        .option("header", "true")
        .option("inferSchema", "true")
        .csv(f"s3a://{MY_BUCKET}/{MY_CSV_FILE}")
    )

    print("Initial rows:", df.count())
    print("Initial partitions:", df.rdd.getNumPartitions())

    # ---- REPARTITION (CRITICAL) ----
    df = df.repartition(200)
    print("Partitions after repartition:", df.rdd.getNumPartitions())

    # ---- PREPARE FEATURES ----
    df_ml = (
        df.select(
            col(MY_SINGLE_NUMERIC_FEATURE).cast("double"),
            col(MY_RESPONSE).cast("double")
        )
    )

    assembler = VectorAssembler(
        inputCols=[MY_SINGLE_NUMERIC_FEATURE],
        outputCol="features"
    )

    df_ml = assembler.transform(df_ml).select(
        col("features"),
        col(MY_RESPONSE).alias("label")
    )

    # ---- DISTRIBUTED LINEAR REGRESSION ----
    lr = LinearRegression(
        featuresCol="features",
        labelCol="label"
    )

    model = lr.fit(df_ml)

    # ---- RESULTS ----
    print("Coefficient:", model.coefficients)
    print("Intercept:", model.intercept)

    spark.stop()


if __name__ == "__main__":
    main()