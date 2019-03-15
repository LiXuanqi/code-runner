from collections import namedtuple

import docker
from docker.errors import ContainerError
import os

client = docker.from_env()

CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))
TEMP_DIR = "%s/tmp" % CURRENT_DIR
HOST_DIR = TEMP_DIR
GUEST_DIR = '/test'
SOURCE_FILE_NAME = "Example"

Language = namedtuple('Language', 'source_file execute_file build_command run_command docker_image')


class Runner:
    languages = {
        'java': Language('Example.java', 'Example', 'javac', 'java', 'openjdk'),
        'python': Language('example.py', 'example.py', None, 'python', 'python')
    }

    def __init__(self, language):
        self.language = language

    def run(self, code):
        lang = self.languages[self.language]
        # - write code to file.
        write_code_to_file(code, lang.source_file)

        if lang.build_command:
            # - compile
            try:
                client.containers.run(
                    image=lang.docker_image,
                    command="%s %s" % (lang.build_command, lang.source_file),
                    volumes={
                        HOST_DIR: {
                            'bind': GUEST_DIR,
                            'mode': 'rw',
                            'auto_remove': True
                        }
                    },
                    working_dir=GUEST_DIR
                )
            except ContainerError as e:
                print(e.stderr)
        # - run
        try:
            log = client.containers.run(
                image=lang.docker_image,
                command="%s %s" % (lang.run_command, lang.execute_file),
                volumes={
                    HOST_DIR: {
                        'bind': GUEST_DIR,
                        'mode': 'rw',
                        'auto_remove': True
                    }
                },
                working_dir=GUEST_DIR
            )
            print(log)
            return log
        except ContainerError as e:
            print(e.stderr)


def write_code_to_file(code, filename):
    file = open("%s/%s" % (TEMP_DIR, filename), "w")  # Create a new file if it does not exist.
    file.write(code)

