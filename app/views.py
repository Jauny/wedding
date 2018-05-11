import logging
from flask import redirect, render_template, request, url_for

from app import app
from app.helpers.logger import log_endpoint
from app.models.invites import Invite

logger = logging.getLogger(__name__)


@app.route('/', methods=['GET'])
@log_endpoint(logger)
def index():
    return render_template('index.html')


@app.route('/menu', methods=['GET'])
@log_endpoint(logger)
def menu():
    return render_template('menu.html')


@app.route('/rooms', methods=['GET'])
@log_endpoint(logger)
def rooms():
    return render_template('rooms.html')


@app.route('/rsvp', methods=['GET', 'POST'])
@log_endpoint(logger)
def rsvp():
    """RSVP to an invitation."""
    invite = None

    if request.method == 'GET':
        email = request.args.get('email')
        if email:
            invite = Invite.getFromEmail(email)

        if not invite:
            logger.info({
                'msg': 'no invite found from email param',
                'email': str(email)})
            return render_template('rsvp.html')

        plusone = Invite.getPlusoneFromInvite(invite)
        if not plusone:
            logger.info({
                'msg': 'no plusone found',
                'email': str(email)})

    elif request.method == 'POST':
        email = request.form.get('email')
        invite = Invite.getFromEmail(email)
        if not invite:
            logger.warning({
                'msg': 'no invite found',
                'email': str(email)})
            return render_template(
                'rsvp.html',
                error='We don\'t have this email. Do you have another email?')

        plusone = Invite.getPlusoneFromInvite(invite)
        if not plusone:
            logger.info({
                'msg': 'no plusone found',
                'email': str(email)})

    return render_template(
        'rsvp-confirm.html',
        invite=invite.get('fields'),
        plusone=plusone.get('fields') if plusone else None)


@app.route('/rsvp_confirm', methods=['GET', 'POST'])
@log_endpoint(logger)
def rsvp_confirm():
    """Confirm RSVP with details."""
    if request.method == 'GET':
        logger.warning({
            'msg': 'received GET to /rsvp_confirm'})
        return redirect(url_for('rsvp'))

    email = request.form.get('email')
    rsvp = request.form.get('rsvp')
    food = request.form.get('food')
    plusone_email = request.form.get('plusone_email')
    plusone_rsvp = request.form.get('plusone_rsvp')
    plusone_food = request.form.get('plusone_food')
    rehearsal = request.form.get('rehearsal')
    comments = request.form.get('comments')

    # update rsvp invite
    resp = Invite.updateRSVPForEmail(email, rsvp, food, rehearsal, comments)
    if resp.get('error', None):
        logger.error({
            'msg': 'error updating rsvp',
            'error': str(resp.error),
            'email': str(email),
            'rsvp': str(rsvp),
            'food': str(food),
            'rehearsal': str(rehearsal),
            'comments': str(comments),
        })
    else:
        logger.info({
            'msg': 'updated rsvp',
            'email': str(email),
            'rsvp': str(rsvp),
            'food': str(food),
            'rehearsal': str(rehearsal),
            'comments': str(comments),
        })

    # update plusone invite
    if plusone_email:
        if plusone_rsvp == 'no' or rehearsal == 'no':
            plusone_rehearsal = 'no'
        else:
            plusone_rehearsal = 'yes'
        resp = Invite.updateRSVPForEmail(
            plusone_email, plusone_rsvp, plusone_food, plusone_rehearsal)
        if resp.get('error', None):
            logger.error({
                'msg': 'error updating plusone',
                'error': str(resp.error),
                'email': str(plusone_email),
                'rsvp': str(plusone_rsvp),
                'food': str(plusone_food),
                'rehearsal': str(plusone_rehearsal)})
        else:
            logger.info({
                'msg': 'updated rsvp',
                'email': str(plusone_email),
                'rsvp': str(plusone_rsvp),
                'food': str(plusone_food),
                'rehearsal': str(plusone_rehearsal)})

    if rsvp == 'yes':
        message = 'Hooray! We will see you in Palm Springs.'
    else:
        message = 'Oh no! We will miss you.'

    return render_template(
        'rsvp_done.html',
        message=message)
