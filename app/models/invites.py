import json
import requests

from app.helpers import airtable


class Invite:
    """Invite model, backed up on Airtable 'invites' table."""
    base_url = '{base_url}/invites{api_key}'.format(
        base_url=airtable.BASE_URL,
        api_key=airtable.API_KEY)

    base_url_post = '{base_url}/invites/{{id}}{api_key}'.format(
        base_url=airtable.BASE_URL,
        api_key=airtable.API_KEY)

    def __init__(self, **kwargs):
        """Init an invite from kwargs."""
        if kwargs:
            for key, value in kwargs.iteritems():
                setattr(self, key, value)

    @classmethod
    def getAll(cls):
        """Return all invites from airtable."""
        resp = requests.get(cls.base_url)
        return json.loads(resp.read()).get('records')

    @classmethod
    def getAllUnsent(cls):
        """Return all unsent invites."""
        data = {
            'filterByFormula': 'NOT({sent})'
        }
        resp = requests.get(
            cls.base_url,
            params=data)
        return resp.json().get('records')

    @classmethod
    def getAllMissingRSVP(cls, offset=None):
        """Return all unsent invites."""
        results = []

        data = {'filterByFormula': '{sent} = ""'}
        if offset:
            data['offset'] = offset

        resp = requests.get(cls.base_url, params=data)
        data = resp.json()

        results += data.get('records')
        while data.get('offset'):
            results += cls.getAllMissingRSVP(cls, offset)

        return results

    @classmethod
    def getFromEmail(cls, email):
        """Return record with email."""
        data = {'filterByFormula': '{email} = "%s"' % email}

        resp = requests.get(cls.base_url, params=data)
        records = resp.json().get('records')
        if records and len(records):
            return records[0]
        else:
            return None

    @classmethod
    def getPlusoneFromInvite(cls, invite):
        """Return plusone invite from invite or None."""
        plusone = invite.get('fields', {}).get('plusone')
        if plusone:
            return cls.getFromEmail(plusone)

        return None

    @classmethod
    def updateRSVPForEmail(cls, email, rsvp, rehearsal):
        """Update invite for email with rsvp."""
        invite = cls.getFromEmail(email)
        if not invite:
            return None

        url = cls.base_url_post.format(id=invite.get('id'))
        data = {
            'fields': {
                'rsvp': rsvp,
                'rehearsal': rehearsal
            }
        }

        resp = requests.patch(
            url=url,
            data=json.dumps(data),
            headers={'Content-Type': 'application/json'})
        return resp.json()
