from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, Pet
from forms import AddPet

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///adoption_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False
app.config['SECRET_KEY'] = "SecretKey"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

connect_db(app)

@app.route('/')
def home_page():
    """Render home page"""
    pets = Pet.query.all()
    print(f'Pets = {pets}')
    return render_template("index.html", pets=pets)

@app.route('/add', methods=["GET", "POST"])
def add_pet():
    """Add pet page & functionality to add pet to database"""
    form = AddPet()

    if form.validate_on_submit():
        name = form.name.data
        species = form.species.data
        age = form.age.data
        notes = form.notes.data
        available = form.available.data
        photo_url = form.photo_url.data
        if not photo_url:
            photo_url = 'https://bitsofco.de/content/images/2018/12/broken-1.png'

        new_pet = Pet(name=name, species=species, photo_url=photo_url, age=age, notes=notes, available=available)

        print(photo_url)

        db.session.add(new_pet)
        db.session.commit()
        return redirect('/')
    else:
        return render_template('add-pet.html', form=form)

@app.route('/pet-details/<pet_id>')
def get_pet_details(pet_id):
    """Get pet details & show on page"""
    pet = Pet.query.get_or_404(pet_id)
    
    return render_template('pet-details.html', pet=pet)

@app.route('/edit/<pet_id>', methods=["GET", "POST"])
def edit_pet_details(pet_id):
    """Get pet details & show on page in editable form"""
    pet = Pet.query.get_or_404(pet_id)
    form = AddPet(obj=pet)
    
    if form.validate_on_submit():
        pet.name = form.name.data
        pet.species = form.species.data
        pet.age = form.age.data
        pet.notes = form.notes.data
        pet.available = form.available.data
        pet.photo_url = form.photo_url.data

        db.session.commit()
        return redirect(f'/pet-details/{pet_id}')

    else:
        return render_template('edit-pet.html', pet=pet, form=form)



    
