import os
from azure.storage.blob import BlobServiceClient

# Set the connection string for both storage accounts
source_connection_string = os.environ["SOURCE_CONNECTION_STRING"]
destination_connection_string = os.environ["DESTINATION_CONNECTION_STRING"]

# Create BlobServiceClient objects for both storage accounts
source_blob_service_client = BlobServiceClient.from_connection_string(source_connection_string)
destination_blob_service_client = BlobServiceClient.from_connection_string(destination_connection_string)

# Define the name of the container to be used for the blobs
container_name = "mycontainer"

# Create the container on both storage accounts if it does not exist
if not source_blob_service_client.get_container_client(container_name).exists():
    source_blob_service_client.create_container(container_name)
if not destination_blob_service_client.get_container_client(container_name).exists():
    destination_blob_service_client.create_container(container_name)

# Upload 100 blobs to the source container
for i in range(1, 101):
    blob_name = f"blob{i}"
    blob_client = source_blob_service_client.get_blob_client(container=container_name, blob=blob_name)
    blob_client.upload_blob(f"Blob {i} content")

# Copy each blob from the source container to the destination container
for i in range(1, 101):
    blob_name = f"blob{i}"
    source_blob_client = source_blob_service_client.get_blob_client(container=container_name, blob=blob_name)
    destination_blob_client = destination_blob_service_client.get_blob_client(container=container_name, blob=blob_name)
    destination_blob_client.start_copy_from_url(source_blob_client.url)
