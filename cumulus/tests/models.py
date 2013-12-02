from django.db import models

from cumulus.storage import SwiftclientStorage


class Thing(models.Model):
    "A dummy model to use for tests."
    image = models.ImageField(upload_to="cumulus-tests",
                              blank=True)
    document = models.FileField(upload_to="cumulus-tests")
    custom = models.FileField(upload_to="cumulus-tests")
