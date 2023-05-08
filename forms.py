from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, EqualTo, InputRequired


class LoginForm(FlaskForm):

    login = StringField('pålogging', validators=[DataRequired(message="Du må angi en pålogging.")])
    password = PasswordField('Passord', validators=[DataRequired(message="Du må angi et passord.")])

    submit = SubmitField('Logg inn')


class RegistrationForm(FlaskForm):

    login = StringField('Pålogging', validators=[DataRequired(message="Du må angi en pålogging."), Length(min=4, max=25, message="Pålogging må være mellom 4 og 25 tegn.")])
    first_name = StringField('Fornavn', validators=[InputRequired(message="Du må taste inn et fornavn")])
    last_name = StringField('Etternavn', validators=[InputRequired(message="Du må taste inn et etternavn")])
    password = PasswordField('Passord', validators=[DataRequired(message="Du må angi et passord."), Length(min=8, max=25, message="Passord må være mellom 8 og 25 tegn.")])
    password_confirm = PasswordField('Bekreft passord', validators=[
        DataRequired(message="Du må bekrefte passordet."), Length(min=8, max=25, message="Passord må være mellom 8 og 25 tegn."), EqualTo('password', message="Passordene må være like.")
    ])

    submit = SubmitField('Registrer')


class AddCategoryForm(FlaskForm):

    category_name = StringField('Kategori Navn', validators=[DataRequired(message="Du må angi en kategori.")])

    submit = SubmitField('Legg til kategori')
