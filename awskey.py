DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

AWS_ACCESS_KEY_ID = "AKIAS4NQIUJ4SY4GG46A" # 액세스 키
AWS_SECRET_ACCESS_KEY = "jS6tdj/Ybhp46FZIedMrKMGk8DgZ/RXk1KcYS2yU" # 비밀 액세스 키

AWS_REGION = "us-east-1" # AWS 지역

AWS_STORAGE_BUCKET_NAME = "h5fileupload" # 버킷 이름
AWS_S3_CUSTOM_DOMAIN = '%s.s3.%s.amazonaws.com' % (
    AWS_STORAGE_BUCKET_NAME, AWS_REGION)