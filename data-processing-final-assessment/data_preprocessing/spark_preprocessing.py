from pyspark.sql import SparkSession
from pyspark.sql.functions import col, mean, when, isnan
from pyspark.ml.feature import StandardScaler, VectorAssembler

# Initialize Spark
spark = SparkSession.builder.appName("DataPreprocessing").getOrCreate()

# Load raw data
df = spark.read.csv("sample_data.csv", header=True, inferSchema=True)

print("Initial Schema:")
df.printSchema()

# Handle missing values
for c in df.columns:
    df = df.withColumn(c, when(isnan(col(c)) | col(c).isNull(), None).otherwise(col(c)))

df = df.na.fill({"age": 30, "income": 40000})  # Example

# Remove duplicates
df = df.dropDuplicates()

# Data type consistency
df = df.withColumn("age", col("age").cast("int"))
df = df.withColumn("income", col("income").cast("float"))

# Normalization
assembler = VectorAssembler(inputCols=["income", "age"], outputCol="features")
df_vector = assembler.transform(df)
scaler = StandardScaler(inputCol="features", outputCol="scaled_features", withStd=True, withMean=False)
scaled_data = scaler.fit(df_vector).transform(df_vector)

# Feature Engineering
final_df = scaled_data.withColumn("income_to_age_ratio", col("income") / (col("age") + 1))

final_df.show(10, truncate=False)
spark.stop()
