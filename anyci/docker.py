"""
Add-on facilitating docker use on CI services.

It allows to load an image from local cache, pull and save back using
a convenience one-liner.

Usage::

    docker.py load-pull-save [-h] [--cache-dir CACHE_DIR]
                                  NAME[:TAG|@DIGEST]

Example::

    $ python anyci/docker.py load-pull-save hello-world:latest
    [anyci:docker.py] Cached image filename: /home/jcfr/docker/hello-world-latest.tar
    [anyci:docker.py] Cached image ID filename: /home/jcfr/docker/hello-world-latest.image_id
    [anyci:docker.py] Cached image not found
    [anyci:docker.py] Pulling image: hello-world:latest
    latest: Pulling from library/hello-world
    Digest: sha256:0256e8a36e2070f7bf2d0b0763dbabdd67798512411de4cdcf9431a1feb60fd9
    Status: Image is up to date for hello-world:latest
    [anyci:docker.py] Current image ID: sha256:c54a2cc56cbb2f04003c1cd4507e118af7c0d340fe7e2720f70976c4b75237dc

    [anyci:docker.py] Caching image into: /home/jcfr/docker
    [anyci:docker.py] Saving image ID into: /home/jcfr/docker/hello-world-latest.image_id

Notes:

- Image is saved into the cache only if needed. In addition to the image
  archive (e.g `image-name.tar`), a file containing the image ID is also
  saved into the cache directory (e.g `image-name.image_id`). This allows
  to quickly read back the image ID of the cached image and determine if
  the current image should be saved into the cache.

"""  # noqa: E501

import argparse
import os
import re
import subprocess
import sys


def _log(*args):
    script_name = os.path.basename(__file__)
    print("[anyci:%s] " % script_name + " ".join(args))
    sys.stdout.flush()


def get_valid_filename(s):
    """
    Returns the given string converted to a string that can be used for a clean
    filename. Specifically, leading and trailing spaces are removed; other
    spaces are converted to underscores; slashes and colons are converted to
    dashes; and anything that is not a unicode alphanumeric, dash, underscore,
    or dot, is removed.
    >>> get_valid_filename("john's portrait in 2004.jpg")
    'johns_portrait_in_2004.jpg'
    >>> get_valid_filename("library/hello-world:latest")
    'library-hello-world-latest'

    Copied from https://github.com/django/django/blob/20be1918e77414837178d6bf1657068c8306d50c/django/utils/encoding.py
    Distributed under BSD-3 License
    """  # noqa: E501
    s = s.strip().replace(' ', '_').replace('/', '-').replace(':', '-')
    return re.sub(r'(?u)[^-\w.]', '', s)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(help='sub-command help')

    # create the parser for the "load-pull-save" command
    parser_pull = subparsers.add_parser("load-pull-save",
                                        help="load-pull-save help")
    parser_pull.add_argument(
        "image", type=str, metavar="NAME[:TAG|@DIGEST]",
        help="Load an image from local cache, pull and save back"
    )

    parser_pull.add_argument(
        "--cache-dir", type=str, metavar="CACHE_DIR", default="~/docker",
        help="Image cache directory (default: ~/docker)"
    )

    args = parser.parse_args()

    if hasattr(args, 'image'):

        # If needed, create cache directory
        cache_dir = os.path.expanduser(args.cache_dir)
        if not os.path.exists(cache_dir):
            os.mkdir(cache_dir)

        # Convert image to valid filename
        filename = os.path.join(cache_dir, get_valid_filename(args.image))
        image_filename = filename + '.tar'
        _log("Cached image filename:", image_filename)
        image_id_filename = filename + '.image_id'
        _log("Cached image ID filename:", image_id_filename)

        # If it exists, load cache image
        cached_image_id = ""
        if os.path.exists(image_filename):
            cmd = ["docker", "load", "-i", image_filename]
            _log("Loading from cache")
            subprocess.check_call(cmd)

            # Read image id
            if os.path.exists(image_id_filename):
                with open(image_id_filename) as content:
                    cached_image_id = content.readline()
                _log("Cached image ID:", cached_image_id)

        else:
            _log("Cached image not found")

        # Pull latest image if any
        _log("Pulling image:", args.image)
        cmd = ["docker", "pull", args.image]
        subprocess.check_call(cmd)

        # Get ID of current image
        cmd = ["docker", "inspect", "--format='{{.Id}}'", args.image]
        output = subprocess.check_output(cmd).decode("utf-8")
        current_image_id = output
        _log("Current image ID:", current_image_id)

        # Cache image only if updated
        if cached_image_id != current_image_id:
            _log("Caching image into:", cache_dir)
            cmd = ["docker", "save", "-o", image_filename, args.image]
            subprocess.check_call(cmd)
            _log("Saving image ID into:", image_id_filename)
            with open(image_id_filename, "w") as content:
                content.write(current_image_id)
        else:
            _log("Skip caching: pulled image identical")
    else:
        parser.print_usage()

if __name__ == '__main__':
    main()
