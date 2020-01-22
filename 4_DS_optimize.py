#WORK IN PROGRESS!!!!




#This code will train a model based on arguments passed to the Experiments feature of CML.

#args for experiment: wine_hiveS3 gb s3a://ml-field/demo/wine/ us-west-2


from churnexplainer import train
from churnexplainer.data import dataset, load_dataset
import cdsw

#os.environ['MODEL_TYPE'] = 'gb'
os.gentenv('MODEL_TYPE', sys.argv[1])

#os.environ['DATASET'] = 'wine_hiveS3'
os.gentenv('DATASET', sys.argv[2])

#os.environ['S3_BUCKET'] = 's3a://ml-field/demo/wine/'
os.gentenv('S3_BUCKET', sys.argv[3])

#os.environ['S3_BUCKET_REGION'] = 'us-west-2'
os.gentenv('S3_BUCKET_REGION', sys.argv[4])


train_score, test_score, model_path = train.experiment_and_save()

cdsw.track_metric("train_score",round(train_score,2))
cdsw.track_metric("test_score",round(test_score,2))
cdsw.track_metric("model_path",model_path)
cdsw.track_file(model_path)