from flask import Blueprint,url_for,flash,redirect,render_template,request

from app import db
from app.models.pet import Pet
from app.models.user import User
from app.form import CreateForm, PetForm

bp = Blueprint("pets_bp", __name__)

@bp.route("/pets" , methods=['GET','POST'])
def pets():
    if request.method == 'POST':
        search = request.form.get('search')
        sort_by = request.form.get('sort_by')
        if search:
            pets = Pet.query.filter(Pet.name_pet.contains(search)).all()
        else:
            if sort_by == 'birthdate':
                pets = Pet.query.order_by(Pet.birthdate).all()
            elif sort_by == 'name_pet':
                pets = Pet.query.order_by(Pet.name_pet).all()
            elif sort_by == 'race':
                pets = Pet.query.order_by(Pet.race).all()
            elif sort_by == 'username':
                pets = Pet.query.join(User).order_by(User.username).all()
            else:
                pets = Pet.query.all()
    else:
        pets = Pet.query.all()

    users = User.query.all()
    return render_template("pets.html", pets=pets, users=users)

@bp.route('/<username>')
def pet_id(username):
    user = User.query.filter_by(username=username).first()
    pets = Pet.query.filter(user == Pet.user).all()
    return render_template("pet_user.html", pets=pets)

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
