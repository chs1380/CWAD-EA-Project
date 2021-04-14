from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, \
    TextAreaField, SelectField
from wtforms.validators import ValidationError, DataRequired, Length
from flask_babel import _, lazy_gettext as _l
from app.models import User


class EditProfileForm(FlaskForm):
    username = StringField(_l('Username'), validators=[DataRequired()])
    about_me = TextAreaField(_l('About me'),
                             validators=[Length(min=0, max=140)])
    submit = SubmitField(_l('Submit'))

    def __init__(self, original_username, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)
        self.original_username = original_username

    def validate_username(self, username):
        if username.data != self.original_username:
            user = User.query.filter_by(username=self.username.data).first()
            if user is not None:
                raise ValidationError(_('Please use a different username.'))


class EditPostForm(FlaskForm):
    body = StringField(_l('Post'), validators=[DataRequired()])
    submit = SubmitField(_l('Submit'))


class PostForm(FlaskForm):
    category = SelectField(u'請選台 吹水台=1, 感情台=2, 黑洞=3',
                           choices=[('1','casual'), ('2', 'relationship'), ('3','blackhole')])
    post = TextAreaField(_l('內容'), validators=[DataRequired()])
    submit = SubmitField(_l('Submit'))


class NewReply(FlaskForm):
    message = TextAreaField('Comment')
