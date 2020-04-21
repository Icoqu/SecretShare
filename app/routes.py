import json
from flask import render_template, flash, redirect, url_for, request
from app.forms import SecretForm, ReadSecretForm
from app import app
from models import Secret


@app.route("/secret", methods=['GET', 'POST'])
@app.route("/secret/", methods=['GET', 'POST'])
def index():
    form = SecretForm()
    if form.validate_on_submit():
        flash('Secret created!')
        secret = Secret(form.secret.data, form.ttl.data, passphrase=form.passphrase.data)
        secret_id = secret.save()
        return redirect('/secret/' + secret_id + '/admin')
    return render_template('index.html', title='Create your secret now!', form=form)


@app.route('/')
def index_redirect():
    return redirect(url_for('index'))


@app.route("/secret/<secret_id>", methods=['GET', 'POST', 'DELETE'])
@app.route("/secret/<secret_id>/", methods=['GET', 'POST', 'DELETE'])
def read_secret(secret_id: str):
    s = Secret.load(secret_id)
    if request.method == 'DELETE':
        s.destroy()
        return 'Ok'
    if s:
        passphrase = s.passphrase
        form = ReadSecretForm()
        if form.validate_on_submit():
            secret = s.read(passphrase=form.passphrase.data)
            return json.dumps({'secret': secret})
    else:
        form = False
        passphrase = False
    return render_template('secret.html', passphrase=passphrase, secret_id=secret_id, form=form)


@app.route("/secret/<secret_id>/admin")
@app.route("/secret/<secret_id>/admin/")
def secret_admin(secret_id):
    secret = Secret.load(secret_id)
    return render_template('secret_admin.html', secret=secret, secret_id=secret_id)
