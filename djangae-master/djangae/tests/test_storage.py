# coding: utf-8
# STANDARD LIB
import os

# THIRD PARTY
import requests
from django.core.files.base import (
    ContentFile,
    File,
)
from django.db import models
from django.test.utils import override_settings
from django.utils import six

# DJANGAE
from djangae.contrib import sleuth
from djangae.storage import (
    CloudStorage,
    _get_storage_client,
)
from djangae.test import TestCase


class ModelWithTextFile(models.Model):
    class Meta:
        app_label = "djangae"

    text_file = models.FileField()


class ModelWithUploadTo(models.Model):
    class Meta:
        app_label = "djangae"

    text_file = models.FileField(upload_to="nested/document/")


class CloudStorageTests(TestCase):

    def setUp(self):
        requests.get('{}/wipe'.format(os.environ["STORAGE_EMULATOR_HOST"]))
        client = _get_storage_client()
        client.create_bucket('test_bucket')
        return super().setUp()

    def test_no_config_raises(self):
        from django.core.exceptions import ImproperlyConfigured

        with sleuth.fake("djangae.storage.project_id", return_value=None):
            with self.assertRaises(ImproperlyConfigured):
                CloudStorage()

    @override_settings(CLOUD_STORAGE_BUCKET='test_bucket')
    def test_basic_actions(self):
        content = b'content'
        storage = CloudStorage()
        name = u'tmp.ąćęłńóśźż.马铃薯.zip'

        f = ContentFile(content, name='my_file')
        filename = storage.save(name, f)
        self.assertIsInstance(filename, six.string_types)
        self.assertTrue(filename.endswith(name))

        self.assertTrue(storage.exists(filename))
        self.assertEqual(storage.size(filename), len(content))
        url = storage.url(filename)
        self.assertIsInstance(url, six.string_types)
        self.assertNotEqual(url, '')

        response = requests.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, content)

        f = storage.open(filename)
        self.assertIsInstance(f, File)
        self.assertEqual(f.read(), content)

        # Delete it
        storage.delete(filename)
        self.assertFalse(storage.exists(filename))

    @override_settings(CLOUD_STORAGE_BUCKET='test_bucket')
    def test_dotslash_prefix(self):
        storage = CloudStorage()
        name = './my_file'
        f = ContentFile(b'content')
        filename = storage.save(name, f)
        self.assertEqual(filename, name.lstrip("./"))

    @override_settings(CLOUD_STORAGE_BUCKET='test_bucket')
    def test_different_bucket(self):
        from google.cloud.exceptions import NotFound
        storage = CloudStorage(bucket_name='different_test_bucket')
        name = './my_file'
        f = ContentFile(b'content')

        with self.assertRaises(NotFound) as cm:
            storage.save(name, f)

        self.assertIn('different_test_bucket', cm.exception.message)

    @override_settings(CLOUD_STORAGE_BUCKET='different_test_bucket')
    def test_different_bucket_config(self):
        from google.cloud.exceptions import NotFound
        storage = CloudStorage()
        name = './my_file'
        f = ContentFile(b'content')

        with self.assertRaises(NotFound) as cm:
            storage.save(name, f)

        self.assertIn('different_test_bucket', cm.exception.message)

    @override_settings(CLOUD_STORAGE_BUCKET='test_bucket')
    def test_supports_nameless_files(self):
        storage = CloudStorage()
        f2 = ContentFile(b'nameless-content')
        storage.save('tmp2', f2)

    @override_settings(CLOUD_STORAGE_BUCKET='test_bucket')
    def test_new_objects_get_the_default_acl(self):
        storage = CloudStorage()
        filename = 'example.txt'
        fileobj = ContentFile(b'content')

        with sleuth.watch('google.cloud.storage.blob.Blob.upload_from_file') as upload_func:
            storage.save(filename, fileobj)

        self.assertTrue(storage.exists(filename))
        self.assertIsNone(upload_func.calls[0].kwargs['predefined_acl'])

    @override_settings(CLOUD_STORAGE_BUCKET='test_bucket')
    def test_new_objects_with_an_explicit_acl(self):
        storage = CloudStorage(google_acl='publicRead')
        filename = 'example.txt'
        fileobj = ContentFile(b'content', name=filename)

        with sleuth.watch('google.cloud.storage.blob.Blob.upload_from_file') as upload_func:
            storage.save(filename, fileobj)

        self.assertTrue(storage.exists(filename))
        self.assertEqual(
            upload_func.calls[0].kwargs['predefined_acl'],
            'publicRead',
        )

    @override_settings(
        CLOUD_STORAGE_BUCKET='test_bucket',
        DEFAULT_FILE_STORAGE='djangae.storage.CloudStorage',
    )
    def test_works_with_text_file_fields(self):
        content = b"content"
        instance = ModelWithTextFile(
            text_file=ContentFile(content, name="my_file")
        )

        instance.save()
        fetched = ModelWithTextFile.objects.get()
        self.assertEqual(fetched.text_file.read(), content)

    @override_settings(
        CLOUD_STORAGE_BUCKET='test_bucket',
        DEFAULT_FILE_STORAGE='djangae.storage.CloudStorage',
    )
    def test_works_with_upload_to(self):
        content = b"content"
        instance = ModelWithUploadTo(
            text_file=ContentFile(content, name="my_file")
        )

        instance.save()
        fetched = ModelWithUploadTo.objects.get()
        self.assertEqual(fetched.text_file.read(), content)

    @override_settings(CLOUD_STORAGE_BUCKET='test_bucket')
    def test_open_uses_correct_bucket(self):
        storage = CloudStorage()
        filename = storage.save('file1', ContentFile(b'content', name='file1'))

        storage = CloudStorage()  # new instance
        storage._open(filename)

    @override_settings(CLOUD_STORAGE_BUCKET='test_bucket')
    def test_delete_uses_correct_bucket(self):
        storage = CloudStorage()
        filename = storage.save('file1', ContentFile(b'content', name='file1'))

        storage = CloudStorage()  # new instance
        storage.delete(filename)
        self.assertFalse(storage.exists(filename))
