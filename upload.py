from google.cloud import storage
import sys

dir = sys.argv[1]
year = sys.argv[2]
month = sys.argv[3]
name = sys.argv[4]
extension = sys.argv[5]



def upload_blob(bucket_name, source_file_name, destination_blob_name):
    """Uploads a file to the bucket."""
    storage_client = storage.Client(project="cctv-media")
    bucket = storage_client.get_bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    blob.upload_from_filename(source_file_name)

    print('File {} uploaded to {}.'.format(
        source_file_name,
        destination_blob_name))

upload_blob('cctv-library', dir+name, "cctv/library/" + year + "/" + month + "/" + name + "/" + name + extension)