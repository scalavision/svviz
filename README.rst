.. image:: https://raw.githubusercontent.com/svviz/svviz/master/docs/example.png
    :width: 80%
    :align: center

*****
svviz
*****

Author: Noah Spies

|
|

**svviz version 2.0** is available here: `https://github.com/nspies/svviz2 <https://github.com/nspies/svviz2>`_ with `documentation here <https://svviz2.readthedocs.io/en/latest/>`_. For most purposes, I recommend using the new version.

|
|
|

``svviz`` visualizes high-throughput sequencing data relevant to a structural variant. Only reads supporting the variant or the reference allele will be shown. svviz can operate in both an interactive web browser view to closely inspect individual variants, or in batch mode, allowing multiple variants (annotated in a VCF file) to be analyzed simultaneously.

Visit the `project site <http://svviz.github.io/svviz/>`_ for a tour of the features and example output.


.. _pypi: http://svviz.readthedocs.io/en/latest/install.html


    
Quickstart
==========

svviz has been tested on Mac OS X and Linux, and should work on Windows, although that has not been tested.

1. Ensure that you have a working compiler by following `these instructions <http://railsapps.github.io/xcode-command-line-tools.html>`_ (OS X only) and that `python <http://docs.python-guide.org/en/latest/>`_ and the python package `pip <https://pip.pypa.io/en/latest/installing.html>`_ are installed.
2. Install the latest version of svviz from github using the following terminal command: ``sudo pip install -U svviz``. (The sudo may not be necessary depending on your setup.)
3. Run the following command, which downloads example data and runs it through svviz: ``svviz demo``. After several processing steps, a web browser window should open, with separate, interactive views of the reference and alternate alleles.

See the `documentation <http://svviz.readthedocs.io/>`_ for more detailed help, or run ``svviz -h`` to get help on command line arguments.

Please submit bug reports or feature requests on the `github issue tracker <https://github.com/svviz/svviz/issues>`_.

Publication
-----------

svviz has been `published in Bioinformatics <http://dx.doi.org/10.1093/bioinformatics/btv478>`_. If you found svviz useful for your research, please cite svviz as follows:

Spies N, Zook JM, Salit M, Sidow A. 2015. svviz: a read viewer for validating structural variants. Bioinformatics doi:bioinformatics/btv478.
