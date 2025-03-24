from flask import Flask, render_template, request, send_from_directory, redirect, url_for
import os
from flask_cors import CORS
from flask_wtf import FlaskForm
from wtforms import FileField, StringField, PasswordField, SubmitField, validators
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_admin.form.upload import ImageUploadField
from flask_login import LoginManager, login_user, login_required, logout_user, current_user, UserMixin

app = Flask(__name__)
CORS(app)

app.config['UPLOAD_FOLDER'] = 'uploads'
app.config["SECRET_KEY"] = "secret_key"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite3"
app.config["UPLOAD_FOLDER"] = "uploads"

db = SQLAlchemy(app)
admin = Admin(app, endpoint="/zfkrvjl323", template_mode="bootstrap3")
login_manager = LoginManager(app)
login_manager.login_view = "login"
login_manager.login_message = "You didn't log in"

# Models

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)

class PostImage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=True)
    image = db.Column(db.String(255), nullable=False)

# Views

class PostImageView(ModelView):
    form_extra_fields = {
        'image': ImageUploadField('image', base_path="uploads")
    }

    def on_model_delete(self, model):
        if model.image:
            image_path = os.path.join(app.config['UPLOAD_FOLDER'], model.image)
            if os.path.exists(image_path):
                os.remove(image_path)

# Forms

class LoginForm(FlaskForm):
    name = StringField("name", validators=[validators.DataRequired()])
    username = StringField("username", validators=[validators.DataRequired()])
    password = PasswordField("password", validators=[validators.DataRequired()])
    submit = SubmitField("submit")

class ImageForm(FlaskForm):
    image = FileField("image", validators=[validators.DataRequired()])

admin.add_view(PostImageView(PostImage, db.session))
admin.add_view(ModelView(User, db.session))

with app.app_context():
    db.create_all()

if not os.path.exists("uploads"):
    os.makedirs("uploads")

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route("/", methods=["GET", "POST"])
def Home():
    if request.method == "POST":
        if 'image' not in request.files:
            return "No file uploaded"
        file = request.files['image']
        file.save(f"uploads/{file.filename}")

    images = os.listdir("uploads")

    all_images = PostImage.query.all()
    
    return render_template("index.html", images=images, all_images=all_images, user=current_user)

@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        name = form.name.data
        username = form.username.data
        password = form.password.data
        user = User.query.filter_by(name=name, username=username, password=password).first()
        if not user:
            user = User(name=name, username=username, password=password)
            db.session.add(user)
            db.session.commit()
        login_user(user)
        return redirect(url_for("Home"))
    return render_template("login.html", form=form)

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("Home"))

@app.route("/uploads/see/<int:image_id>")
@login_required
def send_image(image_id):
    image = PostImage.query.get(image_id)
    return render_template("see.html", image=image)

@app.route("/uploads/see/url/<image>")
def image_url(image):
    return send_from_directory("uploads", image)


app.run(debug=True, host="0.0.0.0", port=5500)
