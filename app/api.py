from flask import Blueprint,request, jsonify

from app.models.pet import Pet
from app.models.user import User
from app.form import CreateForm, PetForm


bp = Blueprint("api_bp", __name__)

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

    if not pets:
        return jsonify({'error': 'No pets found'}), 404
        
    return jsonify([pet.to_dict() for pet in pets])

@bp.route('/pets/<username>', methods=['GET'])
def pet_id(username):
    user = User.query.filter_by(username=username).first()
    if not user:
        return jsonify({'error': 'User not found'}), 404
    pets = Pet.query.filter(user == Pet.user).all()
    if not pets:
        return jsonify({'error': 'No pets found'}), 404
    return jsonify([pet.to_dict() for pet in pets])

@bp.route("/pets", methods=['POST'])
def create_pet():
    form = PetForm()
    users = User.query.all()
    form.user_id.choices = [(user.id, user.username) for user in users]
    if form.validate_on_submit():
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
        return jsonify({'message': 'Pet created successfully'}), 201
    return jsonify({'error': 'Validation error', 'errors': form.errors}), 400

@bp.route("/post/update/<int:id>", methods=['GET','POST'])
def update_pet(id):
    pet = Pet.query.get(id)
    if request.method == 'POST':
        user_id = request.json.get('user_id')
        if pet.user_id == user_id:
            pet.name_pet = request.json.get('name_pet')
            pet.race = request.json.get('race')
            pet.birthdate = request.json.get('birthdate')
            db.session.commit()
            return jsonify({'message': 'Successfully updated pet'})
        else:
            return jsonify({'message': 'You cannot modify the form'})
    return jsonify({
        'name_pet': pet.name_pet,
        'race': pet.race,
        'birthdate': pet.birthdate,
        'owner_id': pet.user_id
    })