django-cumulus
==============

The aim of django-cumulus is to provide a set of tools to utilize the
python-swiftclient api through Django. It currently includes a
custom file storage class, SwiftclientStorage.

.. image:: https://travis-ci.org/richleland/django-cumulus.png?branch=master

Documentation
*************

For full documentation, go to http://django-cumulus.rtfd.org/.


Development
***********

To run the unit-tests locally, just run `make` which will create
a virtualenv and then run the test target.

To run the integration tests you'll need to first install
some extra dependencies in the virtualenv:

```
 $ make integration-dependencies
```

Then export your credentials, for example:

```
 $ export OS_REGION_NAME=RegionOne \
          OS_TENANT_ID=4dce19fd28fb4efc985d63b6d03b46f3 \
          OS_PASSWORD=******** \
          OS_AUTH_URL=http://x.x.x.x:5000/v2.0/ \
          OS_USERNAME=username \
          OS_TENANT_NAME=tenantname \
          PYRAX_IDENTITY_TYPE=keystone
```

then

```
 $ make integration-tests
```
