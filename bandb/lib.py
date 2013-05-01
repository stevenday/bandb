from urlparse import urlsplit, urlunsplit

from django.contrib.staticfiles.storage import CachedFilesMixin

from pipeline.storage import PipelineMixin
from storages.backends.s3boto import S3BotoStorage


class ProtocolRelativeS3BotoStorage(S3BotoStorage):
    """
    Extends S3BotoStorage to return protocol-relative URLs

    From: https://gist.github.com/idan/1638695
    """
    def url(self, name):
        """Modifies return URLs to be protocol-relative."""
        url = super(ProtocolRelativeS3BotoStorage, self).url(name)
        parts = list(urlsplit(url))
        parts[0] = ''
        return urlunsplit(parts)


class S3PipelineStorage(PipelineMixin,
                        CachedFilesMixin,
                        ProtocolRelativeS3BotoStorage):
    # A custom static files storage class that mashes together S3 and Django-Pipeline
    pass
