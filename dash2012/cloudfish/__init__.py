from libcloud.compute.types import Provider

CLOUD_RACKSPACE = 'RS'
CLOUD_AWS = 'AM'

SUPPORTED_CLOUDS = (
    (CLOUD_AWS, 'Amazon Web Services'),
    (CLOUD_RACKSPACE, 'Rackspace Open Cloud'),
)

# FIXME: Show all EC2 Regions
SUPPORTED_PROVIDERS = {
    CLOUD_AWS: [getattr(Provider, attr) for attr in Provider.__dict__ if attr.startswith("EC2_")],
    CLOUD_RACKSPACE: Provider.RACKSPACE,
}