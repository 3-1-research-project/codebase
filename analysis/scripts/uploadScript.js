const { BlobServiceClient, StorageSharedKeyCredential } = require('@azure/storage-blob');
const path = require('path');
const fs = require('fs');

const accountName = '3dash1readings';
const accountKey = '';
const containerName = 'readings';

const dataFolder = path.join(__dirname, '');

const uploadFiles = async () => {
  const sharedKeyCredential = new StorageSharedKeyCredential(accountName, accountKey);
  const blobServiceClient = new BlobServiceClient(
    `https://${accountName}.blob.core.windows.net`,
    sharedKeyCredential
  );

  const containerClient = blobServiceClient.getContainerClient(containerName);

  const files = fs.readdirSync(dataFolder);

  if (files.length === 0) {
    console.log('📁 No files found in ./data to upload.');
    return;
  }

  for (const file of files) {
    const fullPath = path.join(dataFolder, file);
    const blockBlobClient = containerClient.getBlockBlobClient(file);

    console.log(`⬆️ Uploading ${file}...`);
    try {
      const uploadBlobResponse = await blockBlobClient.uploadFile(fullPath);
      console.log(`✅ ${file} uploaded successfully. Request ID: ${uploadBlobResponse.requestId}`);
    } catch (err) {
      console.error(`❌ Error uploading ${file}:`, err.message);
    }
  }

  console.log('✅ All files processed. Succesfully uploaded: ', files.length);
};

uploadFiles();
