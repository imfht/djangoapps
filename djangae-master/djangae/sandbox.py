import logging
import os
import psutil
import signal
import subprocess
import sys
import time
from datetime import datetime
from typing import Optional, Sequence
from urllib.error import (
    HTTPError,
    URLError,
)
from urllib.request import urlopen

from django.utils.autoreload import DJANGO_AUTORELOAD_ENV

from djangae.environment import get_application_root
from djangae.utils import get_next_available_port, port_is_open

_ACTIVE_EMULATORS = {}
_ALL_EMULATORS = ("datastore", "tasks", "storage")

_DJANGO_DEFAULT_PORT = 8000

SERVICE_HOST = "127.0.0.1"
SERVICE_PROTOCOL_HOST = f"http://{SERVICE_HOST}"

DATASTORE_PORT = 10901
TASKS_PORT = 10908
STORAGE_PORT = 10911

DEFAULT_PROJECT_ID = "example"
DEFAULT_BUCKET = "%s.appspot.com" % DEFAULT_PROJECT_ID

logger = logging.getLogger(__name__)


def _launch_process(command_line):
    env = os.environ.copy()
    return subprocess.Popen(command_line.split(" "), env=env)


def _wait_for_tasks(port):
    time.sleep(2)  # FIXME: Need to somehow check it's running


def _wait_for_datastore(port):
    _wait(port, "Cloud Datastore Emulator")


def _wait_for_storage(port):
    _wait(port, "Cloud Storage Emulator")


def _wait(port, service):
    logger.info("Waiting for %s..." % service)

    TIMEOUT = 60.0
    start = datetime.now()

    time.sleep(1)

    failures = 0
    while True:
        try:
            response = urlopen(f"{SERVICE_PROTOCOL_HOST}:{port}/")
        except (HTTPError, URLError):
            failures += 1
            time.sleep(1)
            if failures > 5:
                # Only start logging if this becomes persistent
                logger.exception("Error connecting to the %s. Retrying..." % service)
            continue

        if response.status == 200:
            # Give things a second to really boot
            time.sleep(1)
            break

        if (datetime.now() - start).total_seconds() > TIMEOUT:
            raise RuntimeError("Unable to start %s. Please check the logs." % service)

        time.sleep(1)


def _kill_proc_tree(pid, sig=signal.SIGTERM, timeout=None, on_terminate=None):
    """Kill a process tree (including grandchildren) with signal
    "sig" and return a (gone, still_alive) tuple.
    "on_terminate", if specified, is a callabck function which is
    called as soon as a child terminates.
    """
    assert pid != os.getpid(), "won't kill myself"
    parent = psutil.Process(pid)
    children = parent.children(recursive=True)
    children.append(parent)

    for p in children:
        try:
            p.send_signal(sig)
        except psutil.NoSuchProcess:
            pass
    gone, alive = psutil.wait_procs(children, timeout=timeout, callback=on_terminate)
    return (gone, alive)


def start_emulators(
    persist_data: bool,
    project_id: str = DEFAULT_PROJECT_ID,
    emulators: Sequence[str] = _ALL_EMULATORS,
    datastore_port: int = DATASTORE_PORT,
    datastore_dir: Optional[str] = None,
    tasks_port: int = TASKS_PORT,
    task_target_port: Optional[int] = None,
    autodetect_task_port: bool = True,
    storage_port: int = STORAGE_PORT,
    storage_dir: Optional[str] = None,

):
    # This prevents restarting of the emulators when Django code reload kicks in
    if os.environ.get(DJANGO_AUTORELOAD_ENV) == 'true':
        return

    storage_dir = storage_dir or os.path.join(get_application_root(), ".storage")
    enable_test_environment_variables()

    if "datastore" in emulators:
        if not port_is_open(SERVICE_HOST, datastore_port):
            # If start_emulators is call explicitly passing the Datastore Emulator port
            # and the port is not available raise and Runtime exception.
            if datastore_port != DATASTORE_PORT:
                raise RuntimeError(f"Unable to start Cloud Datastore Emulator at port {datastore_port}.")
            else:
                datastore_port = get_next_available_port(SERVICE_HOST, datastore_port)

        os.environ["DATASTORE_EMULATOR_HOST"] = f"{SERVICE_HOST}:{datastore_port}"
        os.environ["DATASTORE_PROJECT_ID"] = project_id

        # Start the cloud datastore emulator
        command = f"gcloud beta emulators datastore start --user-output-enabled=false --consistency=1.0 --quiet --project={project_id}"  # noqa
        command += f" --host-port={SERVICE_HOST}:{datastore_port}"

        if datastore_dir:
            command += " --data-dir=%s" % datastore_dir
        if not persist_data:
            command += " --no-store-on-disk"

        _ACTIVE_EMULATORS["datastore"] = _launch_process(command)
        _wait_for_datastore(datastore_port)

    if "tasks" in emulators:
        # If start_emulators is call explicitly passing the Cloud Task emulator port
        # and the port is not available raise and Runtime exception.
        if not port_is_open(SERVICE_HOST, tasks_port):
            if tasks_port != TASKS_PORT:
                raise RuntimeError(f"Unable to start Cloud Tasks Emulator at port {tasks_port}.")
            else:
                tasks_port = get_next_available_port(SERVICE_HOST, tasks_port)

        from djangae.tasks import cloud_tasks_location, cloud_tasks_parent_path, cloud_tasks_project
        default_queue = "%s/queues/default" % cloud_tasks_parent_path()

        if task_target_port is None:
            if sys.argv[1] == "runserver" and autodetect_task_port:
                from django.core.management.commands.runserver import Command as RunserverCommand
                parser = RunserverCommand().create_parser('django', 'runserver')
                args = parser.parse_args(sys.argv[2:])
                if args.addrport:
                    task_target_port = args.addrport.split(":")[-1]
                else:
                    task_target_port = _DJANGO_DEFAULT_PORT
            else:
                task_target_port = _DJANGO_DEFAULT_PORT

        command = "gcloud-tasks-emulator start -q --port=%s --target-port=%s --default-queue=%s" % (
            tasks_port, task_target_port, default_queue
        )

        # If the project contains a queue.yaml, pass it to the Tasks Emulator so that those queues
        # can be created (needs version >= 0.4.0)
        queue_yaml = os.path.join(get_application_root(), "queue.yaml")
        if os.path.exists(queue_yaml):
            command += " --queue-yaml=%s --queue-yaml-project=%s --queue-yaml-location=%s" % (
                queue_yaml, cloud_tasks_project(), cloud_tasks_location()
            )

        os.environ["TASKS_EMULATOR_HOST"] = f"{SERVICE_HOST}:{tasks_port}"
        _ACTIVE_EMULATORS["tasks"] = _launch_process(command)
        _wait_for_tasks(tasks_port)

    if "storage" in emulators:
        # If start_emulators is call explicitly passing the Cloud Storage emulator port
        # and the port is not available raise and Runtime exception.
        if not port_is_open(SERVICE_HOST, storage_port):
            if storage_port != STORAGE_PORT:
                raise RuntimeError(f"Unable to start Cloud Storage Emulator at port {storage_port}.")
            else:
                storage_port = get_next_available_port(SERVICE_HOST, storage_port)

        os.environ["STORAGE_EMULATOR_HOST"] = f"http://{SERVICE_HOST}:{storage_port}"
        command = "gcloud-storage-emulator start -q --port=%s --default-bucket=%s" % (
            storage_port, DEFAULT_BUCKET)

        if not persist_data:
            command += " --no-store-on-disk"

        _ACTIVE_EMULATORS["storage"] = _launch_process(command)
        _wait_for_storage(storage_port)


def stop_emulators(emulators=None):
    # This prevents restarting of the emulators when Django code reload kicks in
    if os.environ.get(DJANGO_AUTORELOAD_ENV) == 'true':
        return

    emulators = emulators or _ALL_EMULATORS
    for name, process in _ACTIVE_EMULATORS.items():

        if name in emulators:
            logger.info('Stopping %s emulator with PID %s', name, process.pid)
            _kill_proc_tree(process.pid)


def enable_test_environment_variables():
    """
        Sets up sample environment variables that are available on production
    """

    os.environ.setdefault("GOOGLE_CLOUD_PROJECT", DEFAULT_PROJECT_ID)
    os.environ.setdefault("GAE_APPLICATION", "e~%s" % DEFAULT_PROJECT_ID)
    os.environ.setdefault("GAE_ENV", "development")
