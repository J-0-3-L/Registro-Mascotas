from flask import Blueprint,url_for,flash,redirect,render_template,request

from app import db
from app.models.pet import Pet
from app.models.user import User
from app.form import CreateForm, PetForm

# from flask_login import current_user

bp = Blueprint("pets_bp", __name__)

@bp.route("/pets")
def pets():
    users = User.query.all()
    pets = Pet.query.all()
    return render_template("pets.html", pets= pets , users= users)

@bp.route('/pets/<id>')
def pet_id(id):
    pet = Pet.query.get(id)
    return render_template("pet_user.html", pet=pet)

@bp.route("/pet/create", methods=['GET','POST'])
def create_pet():
    form = PetForm()
    users = User.query.all()
    form.user_id.choices = [(user.id, user.username) for user in users]
    if request.method == 'POST' and form.validate_on_submit():
        name_pet = form.name_pet.data
        race = form.race.data
        birthdate = form.birthdate.data
        user_id = form.user_id.data
        pet = Pet(
            name_pet=name_pet,
            race=race,
            birthdate=birthdate,
            user_id=user_id
        )
        db.session.add(pet)
        db.session.commit()
        flash("Se ha publicado tu registro con exito!")
        return redirect(url_for('pets_bp.pets'))
    return render_template("pet.html" , form=form)

@bp.route("/post/update/<id>", methods=['GET','POST'])
def update_pet(id):
    form = PetForm()
    pet = Pet.query.get(id)
    users = User.query.all()
    form.user_id.choices = [(user.id, user.username) for user in users]
    if request.method == 'POST' and form.validate_on_submit():
        user_id = form.user_id.data
        if pet.user_id == user_id:
            pet.name_pet = form.name_pet.data
            pet.race = form.race.data
            pet.birthdate = form.birthdate.data
            db.session.commit()
            flash("Se ha actualizado con exito!")
            return redirect(url_for('pets_bp.pets'))
        else:
            flash("No puedes modificar el formulario")
    form.name_pet.data = pet.name_pet
    form.race.data = pet.race
    form.birthdate.data = pet.birthdate
    form.user_id.data = pet.user_id
    return render_template("pet.html" , form=form)

# @bp.route('/post/delete/<id>', methods=['GET'])
# def delete_post(id):
#     pet = Pet.query.get(id)
#     if pet.user_id == current_user.id:
#         db.session.delete(pet)
#         db.session.commit()
#         flash("Se ha eliminado con exito!")
#     return redirect(url_for('pets_bp.pets'))
