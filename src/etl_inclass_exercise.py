# Databricks notebook source
# MAGIC %md #### workshop for ETL

# COMMAND ----------

from pyspark.sql.functions import datediff, current_date, avg



# COMMAND ----------

df_laptimes = spark.read.csv('s3://columbia-gr5069-main/raw/lap_times.csv', header=True)

# COMMAND ----------

display(df_laptimes)

# COMMAND ----------

df_driver = spark.read.csv('s3://columbia-gr5069-main/raw/drivers.csv', header=True)
df_driver.count()

# COMMAND ----------

display(df_driver)

# COMMAND ----------

df_driver = df_driver.withColumn("age",datediff(current_date(),df_driver.dob)/365)


# COMMAND ----------

display(df_driver)

# COMMAND ----------

df_lap_drivers = df_driver.select('driverId', 'nationality', 'age', 'forename', 'surname', 'url').join(df_laptimes, on=['driverId'])
display(df_lap_drivers)

# COMMAND ----------

# MAGIC %md
# MAGIC Aggregate by age

# COMMAND ----------

df_lap_drivers = df_lap_drivers.groupby('nationality', 'age').agg(avg('milliseconds'))
display(df_lap_drivers)

# COMMAND ----------

# MAGIC %md #### storing data in S3

# COMMAND ----------



# COMMAND ----------

df_lap_drivers.write.csv('s3://ypn2001-gr5069/processed/in_class_workshop_2024/laptimes_by_drivers.cvs')

# COMMAND ----------


