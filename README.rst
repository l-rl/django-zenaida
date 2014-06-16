Core functionality (forms, styles, etc) shared by littleweaver projects.

Development
=============

Prerequisites
-------------

The installation instructions below assume you have the following software on your machine:

* `Python 2.7.x <http://www.python.org/download/releases/2.7.6/>`_
* `Ruby <https://www.ruby-lang.org/en/installation/>`_ 
* `Pip <https://pip.readthedocs.org/en/latest/installing.html>`_
* `virtualenv <http://www.virtualenv.org/en/latest/virtualenv.html#installation>`_ (optional)
* `virtualenvwrapper <http://virtualenvwrapper.readthedocs.org/en/latest/install.html>`_ (optional)

Installation instructions
-------------------------

If you are using virtualenv or virtualenvwrapper, create and activate an environment. E.g.,

.. code:: bash

    mkvirtualenv zenaida # Using virtualenvwrapper.

Then, to install:

.. code:: bash

    # Clone django-zenaida to a location of your choice.
    git clone https://github.com/littleweaver/django-zenaida.git

    # Install django-zenaida.
    pip install --no-deps -e django-zenaida

    # Install python requirements. This may take a while.
    pip install -r django-zenaida/test_project/requirements.txt

Modifying Littleweaver Form's CSS files requires `SASS <http://sass-lang.com/>`_, `Compass <http://compass-style.org/>`_, and `Bootstrap SASS <http://getbootstrap.com/css/#sass>`_. If you plan to make changes to CSS files, but don't have those installed:

.. code:: bash
    
    gem install bundler # Ensure you have Bundler. May need sudo.
    bundle install --gemfile django-zenaida/Gemfile # Install Ruby requirements.

Get it running
--------------

.. code:: bash

    cd django-zenaida/test_project
    python manage.py syncdb    # Create/sync the database.
    python manage.py runserver # Run the server! 

Then, navigate to ``http://127.0.0.1:8000/`` in your favorite web browser!

Modifying the Styles
--------------------

Do not modify any of the files within ``django-zenaida/static/zenaida/css/``. That directory is managed by Compass. Instead, edit the compass source files in ``django-zenaida/sass/``. You will need to use the Compass command line tool to compile stylesheets. E.g.,

.. code:: bash

    cd django-zenaida/zenaida # Ensure you are in the directory with config.rb.
    compass watch         # Watch the sass directory for changes.

Or use `Compass.app <http://compass.kkbox.com/>`_.

Overriding styles when using Zenaida
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

If you are using Compass and Bootstrap SASS and you want to override any of Bootstrap's variables, then in your SASS directory, make copies of Zenaida's ``django-zenaida/sass/_variables.sass`` and ``django-zenaida/sass/chosen.sass``, and have your stylesheets include Bootstrap SASS dependent on your copied ``_variables.sass`` which is where you should modify Bootstrap variables. (The styles in ``chosen.sass`` make Chosen elements look bootstrappy, so it is unlikely you will want to modify that file, but it needs to be duplicated in order for it to use any variables you change in ``_variables.sass``.)
