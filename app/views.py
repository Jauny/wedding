import logging
from flask import redirect, render_template, request, url_for

from app import app
# from app.models.invites import Invite

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
    # email = request.form.get('email')
    # invite = Invite.getFromEmail(email)
    invite = None

    if not invite:
        return render_template(
            'rsvp.html',
            error='We don\'t have this email. Do you have another email?')

    return render_template('rsvp-confirm.html', invite=invite)


@app.route('/rsvp_confirm', methods=['GET', 'POST'])
def rsvp_confirm():
    """Confirm RSVP with details."""
    if request.method == 'GET':
        return render_template(
            'rsvp-confirm.html',
            name='Jonathan',
            plusone='Jessica')
        # return redirect(url_for('rsvp'))

    rsvp = request.form.get('rsvp')
    plusone = request.form.get('plusone')
    rehearsal = request.form.get('rehearsal')

    # update rsvp invite
    # update plusone invite

    if rsvp == 'yes':
        message = 'Hooray! We will see you in Palm Springs.'
    else:
        message = 'Oh no! We will miss you.'

    return render_template(
        'rsvp_done.html',
        message=message)
