from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField , IntegerField , DateField
from wtforms.validators import DataRequired

class CreateForm(FlaskForm):
    username = StringField("Nombre de usuario", validators=[DataRequired()])
    dni = IntegerField("DNI", validators=[DataRequired()])
    submit = SubmitField("Crear usuario")

class PetForm(FlaskForm):
    name_pet = StringField("Mascota", validators=[DataRequired()])
    race = StringField("Raza" , validators=[DataRequired()])
    birthdate = DateField("Fecha de nacimiento" , validators=[DataRequired()])
    submit = SubmitField("Añadir mascota")
