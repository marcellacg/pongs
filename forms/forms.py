
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Email, EqualTo


class FormularioRegistro(FlaskForm):
    nome = StringField('nome', validators =[DataRequired()])
    email = StringField('email', validators=[DataRequired(),Email()])
    senha1 = PasswordField('senha', validators = [DataRequired()])
    senha2 = PasswordField('confirmar senha', validators = [DataRequired(),EqualTo('senha1')])
    submit = SubmitField('register')

class FormularioLogin(FlaskForm):
    email = StringField('email',validators=[DataRequired(), Email()])
    senha = PasswordField('senha', validators=[DataRequired()])
    remember = BooleanField('Remember Me',validators= [DataRequired()])
    submit = SubmitField('login')