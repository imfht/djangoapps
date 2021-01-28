# Storage

Djangae provides two storage backends. `djangae.storage.CloudStorage` and `djangae.storage.BlobstoreStorage`.

If you've imported `djangae.settings_base.*`, then the default backend is `djangae.storage.CloudStorage`

## Cloud Storage

`djangae.storage.CloudStorage` is a  django storage backend that works with Google Cloud Storage, you can treat it just
as you would with other storage backends. Google Cloud storage is a general purpose storage backend.

To use this you need to [install the `GoogleAppEngineCloudStorageClient` library](https://cloud.google.com/appengine/docs/python/googlecloudstorageclient/using-cloud-storage#downloading_the_client_library).

* Cloud storage will use the default bucket name `CLOUD_STORAGE_BUCKET` unless specified with `BUCKET_KEY` in your settings.py

You can serve files directly from cloudstorage with the key or you can use the included `djangae.storage.serve_file`
* serve_file will create a proxy in the blobstore which can then be used to serve the file, this may be more useful for access control.

### Example usage

Images in this model will be publicly accessible and stored in main bucket of application.

Allowed storage permission levels are defined in [docs -  XML column](https://cloud.google.com/storage/docs/access-control?hl=en#predefined-acl).

```
from django.db import models
from djangae import fields, storage

public_storage = storage.CloudStorage(google_acl='public-read')

class Image(models.Model):
    image_file = models.ImageField(upload_to='/somewhere/', storage=public_storage)

```


## Blobstore

`djangae.storage.BlobstoreStorage` is a storage backend that uses the blobstore, this may be more suitable for temporary file needs
or file processing and is used as a proxy for serving files from Cloud Storage.
