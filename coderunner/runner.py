from collections import namedtuple

import docker
from docker.errors import ContainerError

from .docker_utils import run_docker, TEMP_DIR

client = docker.from_env()

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

        # - compile
        if lang.build_command:
            command = "%s %s" % (lang.build_command, lang.source_file)
            build_success, build_log = run_docker(lang.docker_image, command)

            if not build_success:
                return {
                    'err': build_log,
                }

        # - run
        command = "%s %s" % (lang.run_command, lang.execute_file)
        run_success, run_log = run_docker(lang.docker_image, command)

        if not run_success:
            return {
                'err': run_log
            }
        else:
            return {
                'result': run_log
            }


def write_code_to_file(code, filename):
    file = open("%s/%s" % (TEMP_DIR, filename), "w")  # Create a new file if it does not exist.
    file.write(code)
