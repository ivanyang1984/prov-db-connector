PROV Database Connector
=======================

Introduction
------------

.. image:: https://badge.fury.io/py/prov-db-connector.svg
    :target: https://pypi.python.org/pypi/prov-db-connector
    :alt: PyPI version
.. image:: https://travis-ci.org/DLR-SC/prov-db-connector.svg?branch=master
    :target: https://travis-ci.org/DLR-SC/prov-db-connector
    :alt: Build Status
.. image:: https://coveralls.io/repos/github/DLR-SC/prov-db-connector/badge.svg?branch=master
    :target: https://coveralls.io/github/DLR-SC/prov-db-connector?branch=master
    :alt: Coverage Status
.. image:: https://pyup.io/repos/github/dlr-sc/prov-db-connector/shield.svg
    :target: https://pyup.io/repos/github/dlr-sc/prov-db-connector/
    :alt: Updates


This python module provides a general interface to save `W3C-PROV <https://www.w3.org/TR/prov-overview/>`_ documents into databases.
Currently we support the `Neo4j <https://neo4j.com/>`_ graph database.

We transform a PROV document into a graph structure and the result looks like this:

.. figure:: https://cdn.rawgit.com/dlr-sc/prov-db-connector/master/docs/_images/test_cases/test_prov_primer_example.svg
   :align: center
   :scale: 50 %
   :alt: Complex example in Neo4j

   Complex example in Neo4j

See full documentation at: `prov-db-connector.readthedocs.io <http://prov-db-connector.readthedocs.io>`_

Installation
------------

PyPi
~~~~

Install it by running::

    pip install prov-db-connector

You can view `prov-db-connector on PyPi's package index <https://pypi.python.org/pypi/prov-db-connector/>`_

Source
~~~~~~

.. code:: sh

    # Clone project
    git clone git@github.com:DLR-SC/prov-db-connector.git
    cd prov-db-connector

    # Setup virtual environment
    virtualenv -p /usr/bin/python3.4 env
    source env/bin/activate

    # Install dependencies and package into virtual enviroment
    make setup

Usage
-----

Save and get prov document example
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


.. code-block:: python

    from prov.model import ProvDocument
    from provdbconnector import ProvDb
    from provdbconnector.db_adapters.in_memory import SimpleInMemoryAdapter

    prov_api = ProvDb(adapter=SimpleInMemoryAdapter, auth_info=None)

    # create the prov document
    prov_document = ProvDocument()
    prov_document.add_namespace("ex", "http://example.com")

    prov_document.agent("ex:Bob")
    prov_document.activity("ex:Alice")

    prov_document.association("ex:Alice", "ex:Bob")

    document_id = prov_api.save_document(prov_document)

    print(prov_api.get_document_as_provn(document_id))

    # Output:
    #
    # document
    # prefix
    # ex < http: // example.com >
    #
    # agent(ex:Bob)
    # activity(ex:Alice, -, -)
    # wasAssociatedWith(ex:Alice, ex:Bob, -)
    # endDocument


File Buffer example
~~~~~~~~~~~~~~~~~~~


.. code-block:: python

    from provdbconnector import ProvDb
    from provdbconnector.db_adapters.in_memory import SimpleInMemoryAdapter
    import pkg_resources

    # create the api
    prov_api = ProvDb(adapter=SimpleInMemoryAdapter, auth_info=None)

    # create the prov document from examples
    prov_document_buffer = pkg_resources.resource_stream("examples", "file_buffer_example_primer.json")

    # Save document
    document_id = prov_api.save_document(prov_document_buffer)
    # This is similar to:
    # prov_api.create_document_from_json(prov_document_buffer)

    # get document
    print(prov_api.get_document_as_provn(document_id))

    # Output:

    # document
    # prefix
    # foaf < http: // xmlns.com / foaf / 0.1 / >
    # prefix
    # dcterms < http: // purl.org / dc / terms / >
    # prefix
    # ex < http: // example / >
    #
    # specializationOf(ex:articleV2, ex:article)
    # specializationOf(ex:articleV1, ex:article)
    # wasDerivedFrom(ex:blogEntry, ex:article, -, -, -, [prov:type = 'prov:Quotation'])
    # alternateOf(ex:articleV2, ex:articleV1)
    # wasDerivedFrom(ex:articleV1, ex:dataSet1, -, -, -)
    # wasDerivedFrom(ex:articleV2, ex:dataSet2, -, -, -)
    # wasDerivedFrom(ex:dataSet2, ex:dataSet1, -, -, -, [prov:type = 'prov:Revision'])
    # used(ex:correct, ex:dataSet1, -)
    # used(ex:compose, ex:dataSet1, -, [prov:role = "ex:dataToCompose"])
    # wasDerivedFrom(ex:chart2, ex:dataSet2, -, -, -)
    # wasGeneratedBy(ex:dataSet2, ex:correct, -)
    # used(ex:compose, ex:regionList, -, [prov:role = "ex:regionsToAggregateBy"])
    # used(ex:illustrate, ex:composition, -)
    # wasGeneratedBy(ex:composition, ex:compose, -)
    # wasAttributedTo(ex:chart1, ex:derek)
    # wasGeneratedBy(ex:chart1, ex:compile, 2012 - 03 - 02
    # T10:30:00)
    # wasGeneratedBy(ex:chart1, ex:illustrate, -)
    # wasAssociatedWith(ex:compose, ex:derek, -)
    # wasAssociatedWith(ex:illustrate, ex:derek, -)
    # actedOnBehalfOf(ex:derek, ex:chartgen, ex:compose)
    # entity(ex:article, [dcterms:title = "Crime rises in cities"])
    # entity(ex:articleV1)
    # entity(ex:articleV2)
    # entity(ex:dataSet1)
    # entity(ex:dataSet2)
    # entity(ex:regionList)
    # entity(ex:composition)
    # entity(ex:chart1)
    # entity(ex:chart2)
    # entity(ex:blogEntry)
    # activity(ex:compile, -, -)
    # activity(ex:compile2, -, -)
    # activity(ex:compose, -, -)
    # activity(ex:correct, 2012 - 03 - 31
    # T09:21:00, 2012 - 04 - 01
    # T15:21:00)
    # activity(ex:illustrate, -, -)
    # agent(ex:derek, [foaf:mbox = "<mailto:derek@example.org>", foaf:givenName = "Derek", prov:type = 'prov:Person'])
    # agent(ex:chartgen, [foaf:name = "Chart Generators Inc", prov:type = 'prov:Organization'])
    # endDocument


You find all examples in the `examples <https://github.com/DLR-SC/prov-db-connector/tree/master/examples>`_ folder


Release
-------
Create a new release on github, please use the semver standard for the version number


License
-------

See `LICENSE <https://github.com/DLR-SC/prov-db-connector/blob/master/LICENSE>`_ file


