from pyspark.sql import SparkSession
from pyspark.sql.functions import avg
from pyspark.ml.regression import LinearRegression

spark = SparkSession.builder.appName("KafkaStreamML").getOrCreate()

df = spark.readStream.format("kafka") \
    .option("kafka.bootstrap.servers", "localhost:9092") \
    .option("subscribe", "sensor_data") \
    .load()

df = df.selectExpr("CAST(value AS STRING)")

# Example: Compute rolling average
rolling_avg = df.groupBy().agg(avg("temperature").alias("avg_temp"))

query = rolling_avg.writeStream.outputMode("complete").format("console").start()
query.awaitTermination()
