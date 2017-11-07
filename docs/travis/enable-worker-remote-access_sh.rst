``enable-worker-remote-access.sh``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Enable access to the Travis build worker via netcat.

Prerequisites:

- To make use of this add-on, you first need to:

    1. create an account on https://dashboard.ngrok.com
    2. get the associated token (e.g ``xxxxxxxxxxxxxxxxxxxx``)

Usage:

    - encrypt the environment variable and associated value using the travis client::

        travis-cli encrypt NGROK_TOKEN=xxxxxxxxxxxxxxxxxxxx -r org/repo

    - update ``travis.yml``::

        [...]
        env:
         global:
          - secure: "xyz...abc...dev="
          [...]

        install:
         - [...]
         - wget https://raw.githubusercontent.com/scikit-build/scikit-ci-addons/master/travis/enable-worker-remote-access.sh -O ../enable-worker-remote-access.sh
         - chmod u+x ../enable-worker-remote-access.sh

        script:
         - [...]

        after_success:
         - ../enable-worker-remote-access.sh

        after_failure:
         - ../enable-worker-remote-access.sh

    - next time travis build the project it will download ngrok and setup the tunnel. Output should
      be similar to this one::

          Executing ngrok
          Executing nc
          Authtoken saved to configuration file: /Users/travis/.ngrok2/ngrok.yml
          INFO[06-05|07:11:10] no configuration paths supplied
          INFO[06-05|07:11:10] using configuration at default config path path=/Users/travis/.ngrok2/ngrok.yml
          INFO[06-05|07:11:10] open config file                         path=/Users/travis/.ngrok2/ngrok.yml err=nil
          DBUG[06-05|07:11:10] init storage                             obj=controller mem size=52428800 err=nil
          DBUG[06-05|07:11:10] Dialing direct, no proxy                 obj=tunSess
          [...]
          DBUG[06-05|07:11:10] decoded response                         obj=csess id=7d08567ce4a5 clientid=169864eb02eb6fba5f585bb6d27445cf sid=7
          resp="&{ClientId:... URL:tcp://0.tcp.ngrok.io:18499 Proto:tcp Opts:map[Addr:0.tcp.ngrok.io:18499] Error: Extra:map[Token:xxxxxxxxxxxxxx]}" err=nil

      where the url and port allowing to remotely connect are ``0.tcp.ngrok.io`` and ``18499``.

    - connection with the worker can be established using netcat. In the example
      below the command ``pwd`` and then ``ls`` are executed::

        $ nc 0.tcp.ngrok.io 18499
        pwd
        /Users/travis/build/jcfr/ci-sandbox
        ls
        LICENSE
        README.md
        appveyor.yml
        circle.yml
        images
        ngrok
        pipe
        scripts


.. note::

    To easily install the travis client, you could the dockerized version
    from `jcfr/docker-travis-cli <https://github.com/jcfr/docker-travis-cli>`_.
    It can easily be installed using::

        curl https://raw.githubusercontent.com/caktux/travis-cli/master/travis-cli.sh \
            -o ~/bin/travis-cli && \
        chmod +x ~/bin/travis-cli

Credits:

   - Initial implementation copied from `fniephaus/travis-remote-shell <https://github.com/fniephaus/travis-remote-shell>`_
   - Support for working with recent version of ``netcat`` adapted from `colesbury/travis-remote-shell <https://github.com/colesbury/travis-remote-shell>`_
     and `emulating-netcat-e@stackoverflow <https://stackoverflow.com/questions/6269311/emulating-netcat-e/8161475#8161475>`_.