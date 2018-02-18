from app import config, logger

import urllib2

API_KEY = '?api_key={key}'.format(key=config.get('AIRTABLE_API_KEY'))
BASE_URL = 'https://api.airtable.com/v0/appHYpokKOhNqlM7m'

def build_url(table, id=None):
    """Return full request url for table."""
    base = '{}/{}'.format(BASE_URL, table)
    if id:
      base = '{}/{}'.format(base, id)

    return '{}{}'.format(base, API_KEY)

def get_record(email):
    """Get a record from email."""
    url = '{url}?email={email}'.format(url=build_url('invites'), email=email)
    response = urllib2.urlopen(url)
    data = response.get('records')[0]
    return data

def rsvp(email, response, **kwargs):
    """Updates a row in airtable for email's rsvp."""
    id = get_record(email).get('id')
    url = build_url('invites', id)
    data = {
        'fields': {
            'rsvp': response,
            'extra': kwargs
        }
    }

    urllib2.urlopen(url=url, data=data)
