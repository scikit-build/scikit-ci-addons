"""
Add-on facilitating docker use on CI services.

It allows to load an image from local cache, pull and save back using
a convenience one-liner.

Usage::

    docker.py load-pull-save [-h] [--cache-dir CACHE_DIR]
                                  NAME[:TAG|@DIGEST]

Example::

    $ python anyci/docker.py load-pull-save hello-world:latest
    [anyci:docker.py] Cached image filename: /home/jcfr/docker/hello-worldlatest.tar
    [anyci:docker.py] Cached image not found
    [anyci:docker.py] Pulling image: hello-world:latest
    latest: Pulling from library/hello-world
    Digest: sha256:0256e8a36e2070f7bf2d0b0763dbabdd67798512411de4cdcf9431a1feb60fd9
    Status: Image is up to date for hello-world:latest
    [anyci:docker.py] Caching image into: /home/jcfr/docker

"""

import argparse
import os
import re
import subprocess
import sys


def _log(*args):
    script_name = os.path.basename(__file__)
    print("[anyci:%s] " % script_name + " ".join(args))
    sys.stdout.flush()


def _get_valid_filename(s):
    """
    Returns the given string converted to a string that can be used for a clean
    filename. Specifically, leading and trailing spaces are removed; other
    spaces are converted to underscores; and anything that is not a unicode
    alphanumeric, dash, underscore, or dot, is removed.
    >>> get_valid_filename("john's portrait in 2004.jpg")
    'johns_portrait_in_2004.jpg'

    Copied from https://github.com/django/django/blob/20be1918e77414837178d6bf1657068c8306d50c/django/utils/encoding.py
    Distributed under BSD-3 License
    """  # noqa: E501
    s = s.strip().replace(' ', '_')
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

    if args.image:

        # If needed, create cache directory
        cache_dir = os.path.expanduser(args.cache_dir)
        if not os.path.exists(cache_dir):
            os.mkdir(cache_dir)

        # Convert image to valid filename
        image_filename = os.path.join(
            cache_dir, _get_valid_filename(args.image) + '.tar')
        _log("Cached image filename:", image_filename)

        # If it exists, load cache image
        if os.path.exists(image_filename):
            cmd = ["docker", "load", "-i", image_filename]
            _log("Loading from cache")
            subprocess.check_call(cmd)
        else:
            _log("Cached image not found")

        # Grab latest image if it is different from the loaded one
        _log("Pulling image:", args.image)
        cmd = ["docker", "pull", args.image]
        subprocess.check_call(cmd)

        # Cache image
        _log("Caching image into:", cache_dir)
        cmd = ["docker", "save", args.image, "-o", image_filename]
        subprocess.check_call(cmd)

if __name__ == '__main__':
    main()
