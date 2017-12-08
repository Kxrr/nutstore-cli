NutStore CLI
============

|VERSION| |PYVERSION|

坚果云 WebDAV 命令行工具

A command-line interface for `NutStore`_ based on WebDAV.

Inspired by `http-prompt`_.


Screenshot
-----------

https://asciinema.org/a/T0AwPltSoPZYSYQ7OHQng15rg


Install
-------

**Only works on Python2.7 now**

.. code::

    $ pip install nutstore-cli


How to setup WebDAV on NutStore
-------------------------------

https://github.com/Kxrr/nutstore-cli/blob/master/docs/tutorial.md


Usage
-----
.. code::

    $ nutstore-cli --help


Config
------

Config by a config file
^^^^^^^^^^^^^^^^^^^^^^^

Nutstore-cli will try to load the config file in  ``~/.nutstore.config`` whose format should like `.nutstore.config.example`_

Config by environment variable
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

* NUTSTORE_USERNAME
* NUTSTORE_KEY
* NUTSTORE_WORKING_DIR

Config by pass args to nutstore-cli
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

You can pass args like ``--username=i@example.com`` directly to nutstore-cli


Debugging
---------

Set the environment variable ``DEBUG`` to ``1`` to print the debug output

Contributing
------------

You're highly encouraged to participate in the development of this project.

All the developing works is on the ``dev`` branch.

By the way, because of lack of documents and tests, please feel free to make a issue before developing if you have any questions.

TODO
----

See `TODO.md`_


.. |PYVERSION| image:: https://img.shields.io/badge/python-2.7-blue.svg
.. |VERSION| image:: https://img.shields.io/badge/version-0.4.2-blue.svg
.. |SCREENSHOT| image:: ./docs/sreenshot.png
.. _NutStore: https://www.jianguoyun.com
.. _http-prompt: https://github.com/eliangcs/http-prompt
.. _.nutstore.config.example: https://github.com/Kxrr/nutstore-cli/blob/master/.nutstore.config.example
.. _TODO.md: https://github.com/Kxrr/nutstore-cli/blob/master/TODO.md

