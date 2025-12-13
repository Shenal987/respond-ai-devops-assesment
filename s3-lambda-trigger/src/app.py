import boto3
import os
import zipfile
import logging

s3 = boto3.client("s3")
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    logger.info("Received event: %s", event)

    record = event["Records"][0]
    bucket = record["s3"]["bucket"]["name"]
    key = record["s3"]["object"]["key"]

    file_name = os.path.basename(key)
    download_path = f"/tmp/{file_name}"
    zip_file_path = f"/tmp/{file_name}.zip"
    zip_key = f"compressed/{file_name}.zip"

    try:
        s3.download_file(bucket, key, download_path)
        logger.info("Downloaded %s from %s", key, bucket)

        with zipfile.ZipFile(zip_file_path, "w", zipfile.ZIP_DEFLATED) as zipf:
            zipf.write(download_path, arcname=file_name)
        logger.info("Created zip: %s", zip_file_path)

        s3.upload_file(zip_file_path, bucket, zip_key)
        logger.info("Uploaded zip to %s", zip_key)

        s3.delete_object(Bucket=bucket, Key=key)
        logger.info("Deleted original file: %s", key)

        result = {
            "status": "success",
            "compressed_file": zip_key,
            "deleted_original": key
        }

        logger.info(result)
        return result

    except Exception as e:
        logger.error("Error processing file %s: %s", key, e, exc_info=True)
        result = {
            "status": "failed",
            "error": str(e),
            "file": key
        }

        logger.info(result)
        return result