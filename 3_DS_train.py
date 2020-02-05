# This code will build a new model into the ~/models directory
# To use this new model, change and save the CHURN_MODEL_NAME environment 
# variable


os.environ['DATASET'] = 'wine'
os.environ['MODEL_TYPE'] = 'gb'
#os.environ['S3_BUCKET'] = 's3a://ml-field/demo/wine/'
#os.environ['S3_BUCKET_REGION'] = 'us-west-2'


from explainer import train
os.environ['MODEL_NAME'] = train.train_and_explain_and_save()

