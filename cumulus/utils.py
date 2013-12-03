import pyrax

from cumulus.settings import CUMULUS


def ensure_pyrax_settings():
    """Ensures that pyrax is notified of any pyrax-related settings."""
    if CUMULUS["PYRAX_IDENTITY_TYPE"]:
        pyrax.set_setting("identity_type", CUMULUS["PYRAX_IDENTITY_TYPE"])
    if CUMULUS["AUTH_URL"]:
        pyrax.set_setting("auth_endpoint", CUMULUS["AUTH_URL"])
    if CUMULUS["AUTH_TENANT_ID"]:
        pyrax.set_setting("tenant_id", CUMULUS["AUTH_TENANT_ID"])
