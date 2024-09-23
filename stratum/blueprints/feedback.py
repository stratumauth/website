# Copyright (C) 2024 jmh
# SPDX-License-Identifier: GPL-3.0-only

from flask import Blueprint, current_app, render_template
from flask_wtf import FlaskForm, RecaptchaField
from flask_mail import Message

from wtforms import EmailField, StringField, TextAreaField
from wtforms.validators import DataRequired, Email, Length

from stratum import mail

bp = Blueprint("feedback", __name__)


class FeedbackForm(FlaskForm):
    email = EmailField(
        "email",
        validators=[DataRequired(), Email()],
        render_kw={"placeholder": "example@example.com"},
    )
    subject = StringField(
        "subject",
        validators=[DataRequired(), Length(max=120)],
        render_kw={"placeholder": "Hello"},
    )
    message = TextAreaField("message", validators=[DataRequired(), Length(max=2000)])
    captcha = RecaptchaField()


@bp.route("/feedback", methods=["GET", "POST"])
def feedback():
    form = FeedbackForm()
    success = None

    if form.validate_on_submit():
        recipient = current_app.config["MAIL_RECIPIENT"]
        message = Message(
            f"Stratum: {form.subject.data}",
            html=render_template("message.jinja", content=form.message.data),
            recipients=[recipient],
            reply_to=form.email.data,
        )

        try:
            mail.send(message)
            success = True
        except Exception as e:
            current_app.logger.exception("Failed to send email: %s", e)
            success = False

    return render_template("feedback.jinja", form=form, success=success)
