from flask import render_template, redirect, url_for, flash, request
from app import app, db, tf_model
from app.forms import LoginForm, RegisterForm, DiseaseForm, ChatForm
from app.models import User, Disease
from app.chatbot_logic import predict_disease_text, predict_disease_image, output_labels
from flask_login import current_user, login_user, logout_user, login_required
from urllib.parse import urlparse
import os
import uuid  # For unique filenames

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember.data)
        next_page = request.args.get('next')
        if not next_page or urlparse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Login', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
@login_required
def register():
    if not current_user.is_admin:
        flash('Only admins can register users')
        return redirect(url_for('index'))
    form = RegisterForm()
    if form.validate_on_submit():
        existing_user = User.query.filter_by(username=form.username.data).first()
        if existing_user:
            flash(f'Username "{form.username.data}" already exists. Please choose a different username.')
            return render_template('register.html', title='Register', form=form)
        try:
            user = User(username=form.username.data, is_admin=form.is_admin.data)
            user.set_password(form.password.data)
            db.session.add(user)
            db.session.commit()
            flash('User registered successfully')
            return redirect(url_for('index'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error registering user: {str(e)}')
            return render_template('register.html', title='Register', form=form)
    return render_template('register.html', title='Register', form=form)

@app.route('/')
@app.route('/index')
@login_required
def index():
    if current_user.is_admin:
        return redirect(url_for('admin_dashboard'))
    else:
        return redirect(url_for('chatbot'))

@app.route('/admin_dashboard')
@login_required
def admin_dashboard():
    if not current_user.is_admin:
        flash('Access denied: Admins only')
        return redirect(url_for('index'))
    diseases = Disease.query.all()
    return render_template('admin_dashboard.html', title='Admin Dashboard', diseases=diseases)

@app.route('/add_disease', methods=['GET', 'POST'])
@login_required
def add_disease():
    if not current_user.is_admin:
        flash('Access denied')
        return redirect(url_for('index'))
    form = DiseaseForm()
    if form.validate_on_submit():
        disease = Disease(
            name=form.name.data,
            image_class_name=form.image_class_name.data,
            symptom_en=form.symptom_en.data,
            symptom_hi=form.symptom_hi.data,
            symptom_bn=form.symptom_bn.data,
            symptom_te=form.symptom_te.data,
            prevention_en=form.prevention_en.data,
            prevention_hi=form.prevention_hi.data,
            prevention_bn=form.prevention_bn.data,
            prevention_te=form.prevention_te.data
        )
        db.session.add(disease)
        db.session.commit()
        flash('Disease added successfully')
        return redirect(url_for('admin_dashboard'))
    return render_template('add_disease.html', title='Add Disease', form=form)

@app.route('/edit_disease/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_disease(id):
    if not current_user.is_admin:
        flash('Access denied')
        return redirect(url_for('index'))
    disease = Disease.query.get_or_404(id)
    form = DiseaseForm(obj=disease)
    if form.validate_on_submit():
        form.populate_obj(disease)
        db.session.commit()
        flash('Disease updated successfully')
        return redirect(url_for('admin_dashboard'))
    return render_template('edit_disease.html', title='Edit Disease', form=form)

@app.route('/delete_disease/<int:id>')
@login_required
def delete_disease(id):
    if not current_user.is_admin:
        flash('Access denied')
        return redirect(url_for('index'))
    disease = Disease.query.get_or_404(id)
    db.session.delete(disease)
    db.session.commit()
    flash('Disease deleted successfully')
    return redirect(url_for('admin_dashboard'))

@app.route('/chatbot', methods=['GET', 'POST'])
@login_required
def chatbot():
    if current_user.is_admin:
        flash('Admins should use the dashboard')
        return redirect(url_for('admin_dashboard'))
    form = ChatForm()
    result = None
    labels = None
    image_filename = None
    if form.validate_on_submit():
        symptom = form.symptom.data
        preferred_lang = form.language.data
        image = form.image.data
        text_result = None
        image_result = None

        # Text-based prediction
        if symptom:
            disease, prevention, conf = predict_disease_text(symptom, preferred_lang)
            text_result = {
                'disease': disease,
                'prevention': prevention,
                'confidence': conf * 100,
                'type': 'Text'
            }

        # Image-based prediction
        if image:
            unique_filename = f"upload_{current_user.id}_{uuid.uuid4()}.{image.filename.rsplit('.', 1)[1].lower()}"
            image_path = os.path.join(app.root_path, 'static/uploads', unique_filename)
            image.save(image_path)
            disease, prevention, conf = predict_disease_image(image_path, preferred_lang)
            image_result = {
                'disease': disease,
                'prevention': prevention,
                'confidence': conf * 100,
                'type': 'Image'
            }
            image_filename = unique_filename  # For display in template

        # Prioritize image if confidence higher, or use text
        if text_result and image_result:
            result = image_result if image_result['confidence'] > text_result['confidence'] else text_result
        elif text_result:
            result = text_result
        elif image_result:
            result = image_result

        labels = output_labels.get(preferred_lang, output_labels['en'])

    return render_template('chatbot.html', title='Chatbot', form=form, result=result, labels=labels, image_filename=image_filename)