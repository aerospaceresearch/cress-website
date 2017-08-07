from html.parser import HTMLParser
import requests

from .models import AxText, AxTiming


class MyHTMLParser(HTMLParser):
    axite_id = None

    def handle_starttag(self, tag, attrs):
        attrs_dict = dict(attrs)
        if 'data-axite-id' in attrs_dict:
            self.axite_id = attrs_dict['data-axite-id']


def extract_axite_id(html):
    parser = MyHTMLParser()
    parser.feed(html)
    return parser.axite_id


def ax_timing_create(axtext):
    axite_id = extract_axite_id(axtext._text)
    if not axite_id:
        # without axite_id the value is useless
        return
    difference = (axtext.modified - axtext.created)
    full_generation_roundtrip = difference.microseconds +\
                                difference.seconds * 1e6
    # only to be sure
    assert difference.days == 0
    AxTiming.objects.create(axtext=axtext,
                            axite_id=axite_id,
                            full_generation_roundtrip=full_generation_roundtrip)


def fill_timings():
    # NOTE: this is only called once for old datasets!

    # all datasets in production database with AxText.pk < 3776 use wrong axite_id
    axtexts = AxText.objects.filter(pk__gte=3776)
    for axtext in axtexts:
        if axtext.axtiming_set.count():
            # we already have a timing dataset
            continue
        ax_timing_create(axtext)


def send_timings_to_report_api():
    # NOTE: this is only called once for old datasets
    for axtiming in AxTiming.objects.exclude(return_code=0):
        axtiming.push_to_api()
