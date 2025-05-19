const { BlobServiceClient, StorageSharedKeyCredential } = require('@azure/storage-blob');
const path = require('path');
const fs = require('fs');

const accountName = '3dash1readings';
const accountKey = '';
const containerName = 'readings';

const uploadFiles = async (filepath) => {
  const sharedKeyCredential = new StorageSharedKeyCredential(accountName, accountKey);
  const blobServiceClient = new BlobServiceClient(
    `https://${accountName}.blob.core.windows.net`,
    sharedKeyCredential
  );

  const containerClient = blobServiceClient.getContainerClient(containerName);

  const file = fs.readFileSync(filepath)
  const blockBlobClient = containerClient.getBlockBlobClient(file);
  console.log(`⬆️ Uploading ${file}...`);

  const uploadBlobResponse = await blockBlobClient.uploadFile(fullPath);
  console.log(`✅ ${file} uploaded successfully. Request ID: ${uploadBlobResponse.requestId}`);
};

uploadFiles(path.join(__dirname, 'data.zip'))
