from flask import render_template, url_for, flash, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_email_signup import app, db, modles
from flask_email_signup.forms import SubscribeForm, UnsubscribeForm


@app.route('/', methods=['GET','POST'])
@app.route('/subscribe', methods=['GET','POST'])
def subscribe():
    form = SubscribeForm()
    if form.validate_on_submit():
        recipient = modles.Recipient(email = form.email.data, locality=form.location.data)
        db.session.add(recipient)
        db.session.commit()
        flash(f'{form.email.data} has been signed up!', 'success')
        return redirect(url_for('subscribe'))
    return render_template('subscribe.html', title='Subsribe',form=form)

@app.route('/unsubscribe', methods=['GET','POST'])
def unsubscribe():
    form = UnsubscribeForm()
    if form.validate_on_submit():
        flash(f'{form.email.data} will stop recieving emails', 'success')
        return redirect(url_for('unsubscribe'))
    return render_template('unsubscribe.html', title='Unsubscribe', form=form)
