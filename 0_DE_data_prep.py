#Fetch raw data and create an external Hive table in CDP/CML.

#Data taken from http://...WineNewGBTDataSet.csv
#wget http://.../WineNewGBTDataSet.csv; aws s3 cp WineNewGBTDataSet.csv s3://ml-field/demo/wine/; rm WineNewGBTDataSet.csv

s3_bucket = os.environ.get('S3_BUCKET', "s3a://ml-field/demo/wine/")
s3_bucket_region = os.environ.get('S3_BUCKET_REGION', "us-west-2")

from pyspark.sql import SparkSession
from pyspark.sql.types import Row, StructField, StructType, StringType, IntegerType

spark = SparkSession.builder\
    .appName("Setup Wine Table")\
    .config("spark.yarn.access.hadoopFileSystems",s3_bucket)\
    .config("spark.hadoop.fs.s3a.s3guard.ddb.region", s3_bucket_region)\
    .getOrCreate()

spark.sql("SHOW databases").show()
spark.sql("USE default")
spark.sql("SHOW tables").show()


#spark.sql("DROP TABLE IF EXISTS wine").show()
statement = '''
CREATE EXTERNAL TABLE IF NOT EXISTS `default`.`wine` (
`fixedAcidity` double , 
`volatileAcidity` double , 
`citricAcid` double , 
`residualSugar` double , 
`chlorides` double , 
`freeSulfurDioxide` double , 
`totalSulfurDioxide` double , 
`density` double , 
`pH` double , 
`sulphates` double , 
`Alcohol` double , 
`Quality` string )
ROW FORMAT DELIMITED FIELDS TERMINATED BY ';' 
STORED AS TextFile 
LOCATION 's3a://ml-field/demo/wine/'
'''
spark.sql(statement) 

spark.sql("DESCRIBE TABLE EXTENDED `default`.`wine`").show()
spark.sql("SELECT * FROM `default`.`wine` LIMIT 5").take(5)
    
spark.stop()
