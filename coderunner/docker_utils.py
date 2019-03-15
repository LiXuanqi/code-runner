import docker
from docker.errors import *
import logging
import os

# - Config logger.
logger_format = '%(asctime)-15s %(message)s'
logging.basicConfig(format=logger_format)
logger = logging.getLogger('docker_utils')
logger.setLevel(logging.DEBUG)

client = docker.from_env()

# - Config path.

CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))
TEMP_DIR = "%s/tmp" % CURRENT_DIR
HOST_DIR = TEMP_DIR
GUEST_DIR = '/test'


def get_image(image):
    try:
        client.images.get(image)
        logger.info("Image is found locally.")
    except ImageNotFound:
        logger.info("Image not found locally. Loading from DockerHub...")
        client.images.pull(image)
    except APIError:
        logger.warning("DockerHub is not accessible! Image not found locally!")


def run_docker(image, command):
    try:
        log = client.containers.run(
            image=image,
            command=command,
            volumes={
                HOST_DIR: {
                    'bind': GUEST_DIR,
                    'mode': 'rw',
                    'auto_remove': True
                }
            },
            working_dir=GUEST_DIR
        )
        return True, log
    except ContainerError as e:
        return False, e.stderr
