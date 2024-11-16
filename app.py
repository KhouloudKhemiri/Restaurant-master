import smtplib
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from datetime import datetime

app = Flask(__name__)

# Configurer la base de données SQLite
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'  # Chemin vers le fichier SQLite
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Désactiver la notification des modifications
app.secret_key = 'your_secret_key'  # Clé secrète pour les sessions
db = SQLAlchemy(app)

# Initialiser Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"  # Définir la page de redirection en cas de non-authentification

# Définir le modèle de la table User
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    date_inscription = db.Column(db.DateTime, default=datetime.utcnow)
    num_telephone = db.Column(db.String(15), nullable=True)

    def __repr__(self):
        return f'<User {self.email}>'

# Définir le modèle de la table Order
class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    address = db.Column(db.String(255), nullable=False)
    message = db.Column(db.Text, nullable=True)
    date_commande = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Order {self.id} from {self.name}>'

# Créer la base de données et les tables User et Order
with app.app_context():
    db.create_all()

# Charger l'utilisateur dans Flask-Login
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Route pour l'inscription
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # Récupérer les données du formulaire
        email = request.form['email']
        password = request.form['password']
        age = request.form['age']
        num_telephone = request.form['num_telephone']

        # Créer un nouvel utilisateur
        new_user = User(email=email, password=password, age=age, num_telephone=num_telephone)

        # Ajouter à la base de données
        db.session.add(new_user)
        db.session.commit()

        flash('Registration successful!', 'success')
        return redirect('/login')  # Redirige vers la page de login après l'inscription

    return render_template('register.html')  # Affiche la page d'inscription

# Route pour la page de connexion
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        # Vérifier l'email et le mot de passe dans la base de données
        user = User.query.filter_by(email=email).first()  # Utiliser email comme champ pour login
        if user and user.password == password:
            login_user(user)  # Connecter l'utilisateur
            flash('Login successful!', 'success')
            return redirect(url_for('home'))  # Rediriger vers la page d'accueil
        else:
            flash('Invalid credentials. Please try again.', 'danger')

    return render_template('login.html')  # Affiche la page de login

# Route pour la page d'accueil (page sécurisée)
@app.route('/')
@login_required
def home():
    return render_template('index.html')

# Route pour se déconnecter
@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out!', 'info')
    return redirect(url_for('login'))  # Rediriger vers la page de login

# Routes pour afficher et gérer les utilisateurs
@app.route('/user_list')
@login_required
def user_list():
    users = User.query.all()
    return render_template('user_list.html', users=users)

# Route pour modifier un utilisateur
@app.route('/edit_user/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_user(id):
    user = User.query.get(id)
    if request.method == 'POST':
        user.email = request.form['email']
        user.password = request.form['password']
        user.age = request.form['age']
        user.num_telephone = request.form['num_telephone']

        db.session.commit()
        flash('Utilisateur mis à jour!', 'success')
        return redirect(url_for('user_list'))

    return render_template('edit_user.html', user=user)

# Route pour supprimer un utilisateur
@app.route('/delete_user/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_user(id):
    user = User.query.get(id)
    db.session.delete(user)
    db.session.commit()
    flash('Utilisateur supprimé!', 'danger')
    return redirect(url_for('user_list'))

# Routes pour d'autres pages
@app.route('/index.html')
def index():
    return render_template('index.html')



@app.route('/Menu.html')
def menu():
    return render_template('Menu.html')

@app.route('/Contact.html')
def contact():
    return render_template('Contact.html')



# Route pour afficher le formulaire de livraison et soumettre une commande
@app.route('/submit-order', methods=['POST'])
@login_required
def submit_order():
    # Récupérer les données du formulaire
    name = request.form['name']
    email = request.form['email']  # Vous pouvez aussi utiliser current_user.email si vous voulez récupérer l'email de l'utilisateur connecté
    address = request.form['address']
    message = request.form.get('message', '')

    # Créer un nouvel objet Order
    new_order = Order(name=name, email=email, address=address, message=message)

    # Ajouter à la base de données
    db.session.add(new_order)
    db.session.commit()

    flash('Votre commande a été envoyée avec succès!', 'success')
    return redirect(url_for('order_history'))
# Route pour afficher l'historique des commandes
@app.route('/order-history')
@login_required
def order_history():
    # Récupérer toutes les commandes de l'utilisateur connecté
    orders = Order.query.filter_by(email=current_user.email).all()
    return render_template('order_history.html', orders=orders)

if __name__ == '__main__':
    app.run(debug=True)
