import logging
from flask import redirect, render_template, request, url_for

from app import app
from app.models.invites import Invite

log = logging.getLogger(__name__)


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/rsvp', methods=['GET', 'POST'])
def rsvp():
    """RSVP to an invitation."""
    if request.method == 'GET':
        return render_template('rsvp.html')

    # find invitation for email
    email = request.form.get('email')
    invite = Invite.getFromEmail(email)

    if not invite:
        return render_template(
            'rsvp.html',
            error='We don\'t have this email. Do you have another email?')

    plusone = Invite.getPlusoneFromInvite(invite)

    return render_template(
        'rsvp-confirm.html',
        invite=invite.get('fields'),
        plusone=plusone.get('fields') if plusone else None)


@app.route('/rsvp_confirm', methods=['GET', 'POST'])
def rsvp_confirm():
    """Confirm RSVP with details."""
    if request.method == 'GET':
        return redirect(url_for('rsvp'))

    email = request.form.get('email')
    rsvp = request.form.get('rsvp')
    plusone_email = request.form.get('plusone_email')
    plusone_rsvp = request.form.get('plusone_rsvp')
    rehearsal = request.form.get('rehearsal')

    # update rsvp invite
    Invite.updateRSVPForEmail(email, rsvp, rehearsal)

    # update plusone invite
    if plusone_email:
        if plusone_rsvp == 'no' or rehearsal == 'no':
            plusone_rehearsal = 'no'
        else:
            plusone_rehearsal = 'yes'
        Invite.updateRSVPForEmail(
            plusone_email, plusone_rsvp, plusone_rehearsal)

    if rsvp == 'yes':
        message = 'Hooray! We will see you in Palm Springs.'
    else:
        message = 'Oh no! We will miss you.'

    return render_template(
        'rsvp_done.html',
        message=message)
