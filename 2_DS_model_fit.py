!pip3 install sklearn

import numpy as np
import pandas as pd
import os

#If you created the Hive table in step 0 you can read the data from
#there using Apache Spark (as follows) instead of from local disk.

#from pyspark.sql import SparkSession
#from pyspark.sql.types import Row, StructField, StructType, StringType, IntegerType
#spark = SparkSession.builder
#  .appName("Import Wine Table")    
#  .config("spark.yarn.access.hadoopFileSystems", "s3a://ml-field/demo/wine/")    
#  .config("spark.hadoop.fs.s3a.s3guard.ddb.region", "us-west-2")    
#  .getOrCreate()
#wine_df = spark.sql("SELECT * FROM `default`.`wine`").toPandas()
#spark.stop()

#If you don't read from the Hive Metastore you need to provide the
#schema and read from CSV.

data_dir='/home/cdsw'
csvpath = os.path.join(data_dir, 'raw', 'WineNewGBTDataSet.csv')

col_Names=['fixedAcidity',
 'volatileAcidity',
 'citricAcid',
 'residualSugar',
 'chlorides',
 'freeSulfurDioxide',
 'totalSulfurDioxide',
 'density',
 'pH',
 'sulphates',
 'Alcohol',
 'Quality']

wine_df = pd.read_csv(csvpath, sep=";", header=None, names=col_Names, index_col=None)
wine_df.head()

#check labels
print(wine_df.Quality.unique())

#clean up and encode labels
wine_df.Quality.replace('1',"Excellent",inplace=True)
wine_df.describe()


#encode labels 
wine_df.Quality = pd.Categorical(wine_df.Quality)
wine_df['Label'] = wine_df.Quality.cat.codes
wine_df.head()


#random forest Classifier Grid Search
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test = train_test_split(wine_df.iloc[:,:11],wine_df['Label'],test_size=0.2, random_state=30)

#parameters for grid search
rfc = RandomForestClassifier(random_state=10, n_jobs=-1)

GS_params = { 
    'n_estimators': [25,30,35],
    'max_depth' : [7,9,11]
}

#Cross Validation Grid Search
CV_rfc = GridSearchCV(estimator=rfc, 
                      param_grid=GS_params, 
                      cv= 3, 
                      n_jobs=2,
                      verbose=2)
CV_rfc.fit(X_train, y_train)

#Show Best Parameters 
print(CV_rfc.best_params_)

#final Model
rfc_final= RandomForestClassifier(n_estimators=CV_rfc.best_params_['n_estimators'] , 
                                  max_depth=CV_rfc.best_params_['max_depth'], 
                                  random_state=10, 
                                  n_jobs=2,
                                  verbose=1)
rfc_final.fit(X_train, y_train)
y_true, y_pred = y_test, rfc_final.predict(X_test)


#Evaluation metrics
from sklearn.metrics import classification_report
print(classification_report(y_true, y_pred))


from sklearn.metrics import roc_auc_score
print(roc_auc_score(y_true, y_pred))

