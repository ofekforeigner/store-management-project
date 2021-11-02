from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField, TextAreaField
from wtforms.validators import DataRequired, Length, EqualTo, Email
from wtforms.fields.html5 import DateField
from datetime import date


# user tyeps - manager or not
USER_TYPES = [('1', 'כן'), ('2', 'לא')]

"""
FORMS
"""


class RegisterationForm(FlaskForm):  # REGISTERATION FORM
    name = StringField('שם העובד', validators=[
        DataRequired(), Length(min=2, max=30)])
    username = StringField('שם משתמש', validators=[
                           DataRequired(), Length(min=2, max=20)])
    password = PasswordField('סיסמה', validators=[DataRequired()])
    confirm_password = PasswordField(
        'הכנס סיסמה בשנית', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('הוספת עובד')
    isAdmin = SelectField('האם המשתמש הוא אדמין?', choices=USER_TYPES)


class LoginForm(FlaskForm):  # LOGIN FORM
    username = StringField('שם משתמש', validators=[
        DataRequired(), Length(min=2, max=20)])
    password = PasswordField('סיסמה', validators=[DataRequired()])
    submit = SubmitField('התחבר')


class TaskForm(FlaskForm):  # ADD TASK FORM
    name = SelectField('שם עובד', coerce=str)
    task = StringField('תיאור משימה', validators=[
        DataRequired(), Length(min=2, max=300)])
    task_date = DateField(
        'תאריך לביצוע', default=date.today)
    add_task = SubmitField('הוסף')


class MailForm(FlaskForm):  # SEND MAIL FORM
    name = SelectField('אל', coerce=str)
    header = StringField('נושא', validators=[
        DataRequired(), Length(min=2, max=100)])
    msg = TextAreaField('הודעה', validators=[
        DataRequired(), Length(min=2, max=500)])
    sendMail = SubmitField('שלח')


class FlagForm(FlaskForm):  # FLAG FORM
    task_alert = SelectField('התראת משימות', coerce=str, choices=USER_TYPES)
    items_alert = SelectField('התראת מוצרים שלא בתוקף',
                              coerce=str, choices=USER_TYPES)
    items_amount_alert = SelectField(
        'התראת מלאי של מוצרים', coerce=str, choices=USER_TYPES)
    items_amount = StringField('כמות פריטים להתראה')
    advert = SelectField('תצוגת פרסומות', coerce=str, choices=USER_TYPES)
    sound = SelectField('צלילים', coerce=str, choices=USER_TYPES)
    mail = StringField('כתובת מייל')
    mailpass = PasswordField('סיסמה')
    submit = SubmitField('שמירה')


class ContactForm(FlaskForm):  # ADD CONTACT FORM
    name = StringField('שם מלא', validators=[
        DataRequired(), Length(min=2, max=50)])
    address = StringField('כתובת', validators=[Length(max=20)])
    city = SelectField('עיר', coerce=str)
    phone = StringField('פלאפון', validators=[Length(max=20)])
    mail = StringField("Email")
    submit = SubmitField('הוסף איש קשר')


class ItemsForm(FlaskForm):  # ADD ITEM FORM
    catalogue_number = StringField('מק"ט', validators=[
        DataRequired(), Length(min=2, max=15)])
    name = StringField('שם פריט', validators=[
        DataRequired(), Length(min=2, max=30)])
    amount = StringField('כמות', validators=[Length(max=5)])
    buy_price = StringField('מחיר קניה', validators=[Length(max=5)])
    sell_price = StringField('מחיר מכירה', validators=[Length(max=5)])
    supplier = SelectField('ספק', coerce=str)
    experation_date = DateField(
        'תאריך תפוגה', default=date.today)
    category = SelectField('קטגוריה', coerce=str)
    unit_of_measurment = SelectField('יחידת מידה', coerce=str)
    submit = SubmitField('הוסף פריט')


class SupplierForm(FlaskForm):  # ADD SUPPLIER FORM
    name = StringField('שם ספק', validators=[
        DataRequired(), Length(min=1, max=50)])
    phone = StringField('פלאפון', validators=[Length(max=10)])
    mail = StringField("Email")
    submit = SubmitField('הוסף ספק')
