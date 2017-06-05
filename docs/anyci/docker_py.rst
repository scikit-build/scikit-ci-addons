``docker.py``
^^^^^^^^^^^^^

Add-on facilitating docker use on CI services.

It allows to load an image from local cache, pull and save back using
a convenience one-liner.

Usage::

    ci_addons docker load-pull-save [-h] [--cache-dir CACHE_DIR] [--verbose]
                                         NAME[:TAG|@DIGEST]

Example::

    $ ci_addons docker load-pull-save hello-world:latest
    [anyci:docker.py] Loading cached image from /home/jcfr/docker/hello-world-latest.tar
    [anyci:docker.py]   -> cached image not found
    [anyci:docker.py] Pulling image: hello-world:latest
    [anyci:docker.py]   -> done
    [anyci:docker.py] Reading image ID from current image
    [anyci:docker.py]   -> image ID: sha256:c54a2cc56cbb2f04003c1cd4507e118af7c0d340fe7e2720f70976c4b75237dc
    [anyci:docker.py] Caching image
    [anyci:docker.py]   -> image cached: /home/jcfr/docker/hello-world-latest.tar
    [anyci:docker.py] Saving image ID into /home/jcfr/docker/hello-world-latest.image_id
    [anyci:docker.py]   -> done

.. note::

    - Image is saved into the cache only if needed.

      In addition to the image archive (e.g `image-name.tar`), a file containing
      the image ID is also saved into the cache directory (e.g `image-name.image_id`).

      This allows to quickly read back the image ID of the cached image and determine if
      the current image should be saved into the cache.