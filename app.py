from flask import Flask, render_template, request, send_from_directory, redirect
import os
from flask_cors import CORS
from flask_wtf import FlaskForm
from wtforms import FileField
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_admin.form.upload import ImageUploadField

app = Flask(__name__)
CORS(app)

app.config['UPLOAD_FOLDER'] = 'uploads'
app.config["SECRET_KEY"] = "secret_key"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite3"
app.config["UPLOAD_FOLDER"] = "uploads"

db = SQLAlchemy(app)
admin = Admin(app, endpoint="/zfkrvjl323", template_mode="bootstrap3")

# Models

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
        print(model)
        if model.image:
            image_path = os.path.join(app.config['UPLOAD_FOLDER'], model.image)
            if os.path.exists(image_path):
                os.remove(image_path)

admin.add_view(PostImageView(PostImage, db.session))

with app.app_context():
    db.create_all()

class ImageForm(FlaskForm):
    image = FileField("image")

if not os.path.exists("uploads"):
    os.makedirs("uploads")

@app.route("/", methods=["GET", "POST"])
def Home():
    if request.method == "POST":
        if 'image' not in request.files:
            return "No file uploaded"
        file = request.files['image']
        file.save(f"uploads/{file.filename}")

    images = os.listdir("uploads")

    all_images = PostImage.query.all()

    return render_template("index.html", images=images, all_images=all_images)

@app.route("/uploads/see/<int:image_id>")
def send_image(image_id):
    image = PostImage.query.get_or_404(image_id)
    return render_template("see.html", image=image)

@app.route("/uploads/see/url/<image>")
def image_url(image):
    return send_from_directory("uploads", image)

app.run(debug=True, host="0.0.0.0", port=5500)
