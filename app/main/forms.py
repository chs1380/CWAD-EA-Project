from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, \
    TextAreaField, SelectField
from wtforms.validators import ValidationError, DataRequired, Length
from flask_babel import _, lazy_gettext as _l
from app.models import User


class EditProfileForm(FlaskForm):
    username = StringField(_l('用戶名稱'), validators=[DataRequired()])
    about_me = TextAreaField(_l('關於我'),
                             validators=[Length(min=0, max=140)])
    submit = SubmitField(_l('提交'))

    def __init__(self, original_username, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)
        self.original_username = original_username

    def validate_username(self, username):
        if username.data != self.original_username:
            user = User.query.filter_by(username=self.username.data).first()
            if user is not None:
                raise ValidationError(_('用戶名稱已被註冊'))


class EditPostForm(FlaskForm):
    body = StringField(_l('Post'), validators=[DataRequired()])
    submit = SubmitField(_l('確認'))


class PostForm(FlaskForm):
    category = SelectField(u'選台',
                           choices=[('1','吹水台'), ('2', '感情台'), ('3','黑洞')])
    title = TextAreaField(_l('標題(揀啱分台可避免太快沉底)'), validators=[DataRequired()])
    post = TextAreaField(_l('內容'), validators=[DataRequired()])
    submit = SubmitField(_l('出Post'))


class NewReply(FlaskForm):
    message = TextAreaField('Comment')
