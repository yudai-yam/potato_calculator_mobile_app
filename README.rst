Potato sales calculator
=======================

A mobile app for THE potatoes
------------------------


.. contents:: :local:





Installation
^^^^^^^^^^^^
Run the command below to install the dependencies.
It is recommended to use virtual environment.

.. code-block::

    pip install -e.


Packaging for Android
^^^^^^^^^^^^^^^^^^^^^^
To package the app for Android, use Buildozer.

.. code-block::
    pip install -e.[android-build]
    buildozer init
    buildozer -v android debug
