from pyspark import SparkContext, SparkConf
from pyspark.sql import SparkSession
import os

aws_access_key_id = os.environ['AWS_ACCESS_KEY_ID']
aws_secret_access_key = os.environ['AWS_SECRET_ACCESS_KEY']

# # set conf
conf = (
SparkConf()
    .set("spark.hadoop.fs.s3a.access.key", aws_access_key_id)
    .set("spark.hadoop.fs.s3a.secret.key", aws_secret_access_key)
    .set("spark.hadoop.fs.s3a.fast.upload", True)
    .set("spark.hadoop.fs.s3a.impl", "org.apache.hadoop.fs.s3a.S3AFileSystem")
    .set('spark.hadoop.fs.s3a.aws.credentials.provider', 'com.amazonaws.auth.EnvironmentVariableCredentialsProvider')
    .set('spark.jars.packages', 'org.apache.hadoop:hadoop-aws:3.2.0')
    # .set("spark.hadoop.fs.s3a.access.key", aws_access_key_id)
    # .set("spark.hadoop.fs.s3a.secret.key", aws_secret_access_key)
    # .set("spark.hadoop.fs.s3a.fast.upload", True)
    # .set("spark.hadoop.fs.s3a.impl", "org.apache.hadoop.fs.s3a.S3AFileSystem")
    # .set('spark.hadoop.fs.s3a.aws.credentials.provider', 'com.amazonaws.auth.EnvironmentVariableCredentialsProvider')
    # .set('spark.jars.packages', 'org.apache.hadoop:hadoop-aws:3.2.0')
)

# # apply config
sc = SparkContext(conf=conf).getOrCreate()


if __name__ == "__main__":
    print("PASSEI AQUI")

    # init spark session
    spark = SparkSession\
            .builder\
            .appName("Repartition Job")\
            .getOrCreate()

    spark.sparkContext.setLogLevel("WARN")

    df = (
        spark
        .read
        .format("csv")
        .options(header='true', inferSchema='true', delimiter=';')
        .load("s3a://dl-landing-zone-bronx/titanic/titanic.csv")
    )
    

    df.show()
    df.printSchema()

    (df
    .write
    .mode("overwrite")
    .format("parquet")
    .save("s3a://dl-processing-zone-bronx/titanic")
    )

    print("*****************")
    print("Escrito com sucesso!")
    print("*****************")

    spark.stop()