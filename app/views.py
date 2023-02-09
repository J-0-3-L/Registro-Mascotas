from flask import Blueprint,url_for,flash,redirect,render_template,request

from app import db
from app.models.pet import Pet
from app.models.user import User
from app.form import CreateForm, PetForm

# db.create_all()
bp = Blueprint("views_bp", __name__)

@bp.route("/")
def index():
    return 'Bienvenidos a Cuidando Mascotas'

@bp.route("/users")
def users():
    users = User.query.all()
    return render_template("usuarios.html", users=users)

@bp.route("/user", methods=['GET','POST'])
def add_user():
    form = CreateForm()
    if request.method == 'POST' and form.validate_on_submit():
        username = form.username.data.lower()
        dni = form.dni.data

        existing_user = User.query.filter_by(dni=dni).first()
        if not existing_user:
            user = User(
                username=username,
                dni=dni,
            )
            db.session.add(user)
            db.session.commit()
            flash("El usuario se creó correctamente")
            return redirect(url_for('views_bp.users'))
        else:
            flash("Ya existe un usuario con ese dni")
    return render_template("usuario.html", form=form)
