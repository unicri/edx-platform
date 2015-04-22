"""
Serializers for all Course Descriptor and Course About Descriptor related return objects.

"""
from xmodule.contentstore.content import StaticContent
from django.conf import settings
import sys

DATE_FORMAT = getattr(settings, 'API_DATE_FORMAT', '%Y-%m-%d')


def serialize_content(course_descriptor, about_descriptor):
    """
    Returns a serialized representation of the course_descriptor and about_descriptor
    Args:
        course_descriptor(CourseDescriptor) : course descriptor object
        about_descriptor(dict) : Dictionary of CourseAboutDescriptor objects
    return:
        serialize data for course information.
    """
    data = {
        'media': {},
        'display_name': getattr(course_descriptor, 'display_name', None),
        'course_number': course_descriptor.location.course,
        'course_id': None,
        'advertised_start': getattr(course_descriptor, 'advertised_start', None),
        'is_new': getattr(course_descriptor, 'is_new', None),
        'start': _formatted_datetime(course_descriptor, 'start'),
        'end': _formatted_datetime(course_descriptor, 'end'),
        'announcement': None,
        'effort': about_descriptor.get("effort", None),
        'short_description': about_descriptor.get("short_description", None),
        'description': about_descriptor.get("description", None),
        'key_dates': about_descriptor.get("key_dates", None),
        'video': about_descriptor.get("video", None),
        'course_staff_short': about_descriptor.get("course_staff_short", None),
        'course_staff_extended': about_descriptor.get("course_staff_extended", None),
        'requirements': about_descriptor.get("requirements", None),
        'syllabus': about_descriptor.get("syllabus", None),
        'textbook': about_descriptor.get("textbook", None),
        'faq': about_descriptor.get("faq", None),
        'more_info': about_descriptor.get("more_info", None),
        'number': about_descriptor.get("number", None),
        'instructors': about_descriptor.get("instructors", None),
        'overview': about_descriptor.get("overview", None),
        'end_date': about_descriptor.get("end_date", None),
        'prerequisites': about_descriptor.get("prerequisites", None),
        'ocw_links': about_descriptor.get("ocw_links", None)
    }
    content_id = unicode(course_descriptor.id)
    data["course_id"] = unicode(content_id)
    if getattr(course_descriptor, 'course_image', False):
        data['media']['course_image'] = course_image_url(course_descriptor)

    announcement = getattr(course_descriptor, 'announcement', None)
    data["announcement"] = announcement.strftime(DATE_FORMAT) if announcement else None

    return data


def course_image_url(course):
    """
    Return url of course image.
    Args:
        course(CourseDescriptor) : The course id to retrieve course image url.
    Returns:
        Absolute url of course image.
    """
    loc = StaticContent.compute_location(course.id, course.course_image)
    url = StaticContent.serialize_asset_key_with_slash(loc)
    return url


def _formatted_datetime(course_descriptor, date_type):
    """
    Return formatted date.
    Args:
        course_descriptor(CourseDescriptor) : The CourseDescriptor Object.
        date_type (str) : Either start or end.
    Returns:
        formatted date or None .
    """
    course_date_ = getattr(course_descriptor, date_type, None)
    return course_date_.strftime(DATE_FORMAT) if course_date_ else None
