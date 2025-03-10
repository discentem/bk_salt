import os
import logging

# Set up logging
log = logging.getLogger(__name__)


def tags():
    """
    Custom grain to detect files in /opt/acme/tags and log actions.
    """
    tag_directory = "/opt/bk_salt/tags"
    tags = {}

    log.info("Checking for tag files in %s", tag_directory)

    if os.path.isdir(tag_directory):
        try:
            for tag_file in os.listdir(tag_directory):
                tags[tag_file] = True
                log.debug("Found tag file: %s", tag_file)
        except Exception as e:
            log.error("Error reading tag files: %s", str(e))
    else:
        log.warning("Tag directory does not exist: %s", tag_directory)

    return {"tags": tags}


if __name__ == "__main__":
    print(tags())
