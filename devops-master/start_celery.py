#!/usr/bin/env python
import subprocess


def __external_cmd(cmd, code="utf8"):
    print(cmd)
    process = subprocess.Popen(cmd, shell=True, bufsize=0, stdout=subprocess.PIPE, universal_newlines=True)
    while 1:
        next_line = process.stdout.readline()
        print(next_line.strip())
        if next_line == "" and process.poll() is not None:
            break


if __name__ == '__main__':
    __external_cmd('rm -f logs/celery_worker.pid;export PYTHONOPTIMIZE=1; /home/python372/bin/celery -A devops worker -l info -c 3 '
                   '--max-tasks-per-child 40 --prefetch-multiplier 1 --pidfile logs/celery_worker.pid')
