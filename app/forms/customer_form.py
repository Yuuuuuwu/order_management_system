from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired, Email, Optional

class CustomerForm(FlaskForm):
    class Meta:
        csrf = False    # ← 關掉 CSRF
    name = StringField('姓名', validators=[DataRequired()])
    phone = StringField('電話', validators=[Optional()])
    address = StringField('地址', validators=[Optional()])
    email = StringField('Email', validators=[Optional(), Email()])
    tags = StringField('標籤', validators=[Optional()])  # 逗號分隔
