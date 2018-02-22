import logging
from flask import flash, redirect, render_template, request, url_for

from app import app

log = logging.getLogger(__name__)


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/rsvp', methods=['GET', 'POST'])
def rsvp():
    """RSVP to an invitation."""
    if request.method != 'POST':
        log.warning('received non-POST request to /rsvp')
        return redirect(url_for('index'))
    import pdb; pdb.set_trace()

    # check for missing form elements
    errors = []
    for k, v in request.form.iteritems():
        if len(v) == 0:
            errors.append(k)
    if len(errors) > 0:
        return render_template('index.html', errors=errors)

    rsvp = None

    # if fast rsvp
    if request.form.get('fast-rsvp'):
        rsvp = True if request.form['fast-rsvp'] == "yes" else False
    # if full form
    else:
        pass

    # do something to register the rsvp

    # redirect to index
    if rsvp:
        flash(
            'RSVP registered, see you in Palm Springs ;)')
    else:
        flash(
            'Sorry to hear you won\'t make it. We\'ll have you in spirit! :)')

    return redirect(url_for('index'))
