==========================================
A Python Library for students in Yuanfudao
==========================================

.. image:: https://travis-ci.org/yuantiku/ybckit.svg?branch=master
    :target: https://travis-ci.org/yuantiku/ybckit

This library wraps easygui, matplotlib and media operation for yuanfudao web python environment.

GUI Document
============

ybckit supports the following easygui api for now:

- buttonbox
- enterbox
- passwordbox
- fileopenbox
- diropenbox
- buttonbox

Each of those api has the same method signature expect `root` params because web environment doesn't support it.

For example:

.. code:: python

  import easygui

  easygui.enterbox(msg='Enter something.', title='any title', default='foo')

And run this code:

.. code:: bash

  python -m ybckit.runner test.py

`The full document of easygui can be found here. <http://easygui.sourceforge.net/api.html>`_

License
=======

MIT.
