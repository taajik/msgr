
from pathlib import Path

from django import template
from django.conf import settings
from PIL import Image


register = template.Library()


@register.simple_tag
def get_profile_pic(pic, thumbnail=False):
    """Return url of a suitable profile picture for a user."""

    if pic:
        # The profile picture, if user has one:
        pic_name = pic.name
    else:
        # Or if they don't, the default picture:
        pic_name = "profile_pics/avatar.png"
    pic_name = Path(pic_name)

    # If the picture is needed as a thumbnail:
    if thumbnail:
        # Thumbnail has the same name as the original picture,
        # but it's in the 'thumbnails' subfolder.
        pic_parts = list(pic_name.parts)
        pic_parts.insert(-1, "thumbnails")
        thumbnail_name = Path(*pic_parts)
        thumbnail_path = settings.MEDIA_ROOT / thumbnail_name
        pic_path = settings.MEDIA_ROOT / pic_name
        pic_name = thumbnail_name

        if not thumbnail_path.exists():
            # Create the thumbnail if it doesn't exist;
            # and save it for future use.
            pic = Image.open(pic_path)
            # Its size should be so that the smaller side is 30px.
            r = max(pic.size) / min(pic.size) * 30
            pic.thumbnail((r, r))
            pic.save(thumbnail_path)

    url = settings.MEDIA_URL / pic_name
    return url
