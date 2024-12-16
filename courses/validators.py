from django.core.exceptions import ValidationError
from urllib.parse import urlparse


def validate_video_url(value):
    allowed_domains = ['youtube.com', 'www.youtube.com']
    domain = urlparse(value).netloc
    if domain not in allowed_domains:
        raise ValidationError("Only YouTube links are allowed.")
