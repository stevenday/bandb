from django.contrib.staticfiles.storage import CachedFilesMixin
from pipeline.storage import PipelineMixin
from storages.backends.s3boto import S3BotoStorage


class LessStrictCachedFilesMixin(CachedFilesMixin):
    def hashed_name(self, name, *a, **kw):
        try:
            return super(LessStrictCachedFilesMixin, self).hashed_name(name, *a, **kw)
        except ValueError:
            print 'WARNING: Failed to find file %s. Cannot generate hashed name' % (name,)
            return name


class S3PipelineStorage(PipelineMixin,
                        LessStrictCachedFilesMixin,
                        S3BotoStorage):
    # A custom static files storage class that mashes together S3 and Django-Pipeline
    pass
