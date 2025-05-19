const { BlobServiceClient, StorageSharedKeyCredential } = require('@azure/storage-blob');
const path = require('path');
const fs = require('fs');

const accountName = '3dash1readings';
const accountKey = '';

const downloadFiles = async (containerName, dataFolder) => {
    const sharedKeyCredential = new StorageSharedKeyCredential(accountName, accountKey);
    const blobServiceClient = new BlobServiceClient(
    `https://${accountName}.blob.core.windows.net`,
    sharedKeyCredential
    );

    const containerClient = blobServiceClient.getContainerClient(containerName);

    const downloadPromises = [];

    for await (const blob of containerClient.listBlobsFlat()) {
        // console.log(`Blob: ${blob.name}`);

        if (blob.name.includes("temperature") || blob.name.includes("test")) {
            //console.log(`Blob ${blob.name} is a temperature or test file, skipping download.`);
            continue;
        }

        const blobClient = containerClient.getBlobClient(blob.name);
        const filePath = path.join(dataFolder, blob.name);

        const downloadPromise = (async () => {
            console.log(`Starting download: ${blob.name}`);
            try {
                const downloadResponse = await blobClient.download(0).then((response) => { 
                        if (response._response.status !== 200) {
                            throw new Error(`Failed to download blob: ${response._response.status}`);
                        }
                        return response;
                    }
                );

                await new Promise((resolve, reject) => {
                    downloadResponse.readableStreamBody
                    .pipe(fs.createWriteStream(filePath))
                    .on('finish', resolve)
                    .on('error', (err) => {
                        console.error(`❌ Error writing ${blob.name} to file:`, err.message);
                        reject(err);
                    });
                });
                
                console.log(`✅ ${blob.name} downloaded successfully.`);
            } catch (err) {
                console.error(`❌ Error downloading ${blob.name}:`, err.message);
                return;
            }
        })();
    }

    return await Promise.all(downloadPromises);
};

const dataFolder = path.join(__dirname, 'data');

downloadFiles("python", path.join(dataFolder, 'python'));



