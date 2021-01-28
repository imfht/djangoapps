from django.test import (
    RequestFactory,
    override_settings,
)

from djangae.contrib import sleuth
from djangae.test import TestCase
from djangae.tasks.middleware import _TASK_NAME_HEADER
from ..views import create_datastore_backup


class DatastoreBackupViewTestCase(TestCase):
    """Tests for djangae.contrib.backup.views"""

    @override_settings(DJANGAE_BACKUP_ENABLED=False)
    def test_flag_prevents_backup(self):
        request = RequestFactory().get('/')
        request.META[_TASK_NAME_HEADER] = "test"
        with sleuth.watch('djangae.contrib.backup.views.backup_datastore') as backup_fn:
            create_datastore_backup(request)
            self.assertFalse(backup_fn.called)

    @override_settings(DJANGAE_BACKUP_ENABLED=True)
    def test_get_params_propogate(self):
        request = RequestFactory().get('/?kind=django_admin_log&bucket=foobar')
        request.META[_TASK_NAME_HEADER] = "test"
        with sleuth.fake("djangae.tasks.decorators.is_in_task", True):
            with sleuth.fake('djangae.contrib.backup.views.backup_datastore', None) as backup_fn:
                create_datastore_backup(request)
                self.assertTrue(backup_fn.called)
                self.assertEqual(
                    backup_fn.calls[0][1],
                    {
                        'bucket': 'foobar',
                        'kinds': [u'django_admin_log']
                    }
                )
