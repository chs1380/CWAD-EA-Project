from flask_babel import lazy_gettext as _l, _
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, ValidationError
from wtforms.validators import DataRequired, Email, EqualTo

from app.models import User


class LoginForm(FlaskForm):
    username = StringField(_l('用戶名稱'), validators=[DataRequired()])
    password = PasswordField(_l('密碼'), validators=[DataRequired()])
    remember_me = BooleanField(_l('記住我'))
    submit = SubmitField(_l('登入'))


class RegistrationForm(FlaskForm):
    username = StringField(_l('用戶名稱'), validators=[DataRequired()])
    email = StringField(_l('登入電郵'), validators=[DataRequired(), Email()])
    password = PasswordField(_l('密碼'), validators=[DataRequired()])
    password2 = PasswordField(
        _l('再次輸入密碼'), validators=[DataRequired(),
                                           EqualTo('password')])
    submit = SubmitField(_l('註冊'))

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError(_('用戶名稱已被註冊'))

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError(_('電郵地址已被註冊'))


class ResetPasswordRequestForm(FlaskForm):
    email = StringField(_l('Email'), validators=[DataRequired(), Email()])
    submit = SubmitField(_l('送出'))


class ResetPasswordForm(FlaskForm):
    password = PasswordField(_l('新密碼'), validators=[DataRequired()])
    password2 = PasswordField(
        _l('再次輸入新密碼'), validators=[DataRequired(),
                                           EqualTo('新密碼')])
    submit = SubmitField(_l('重設密碼'))
