from flask import Flask, render_template, redirect, url_for, flash, request, jsonify
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from app import app, db, models
from .forms import SignUpForm, LoginForm, NewReview
import json

login_manager=LoginManager(app)
login_manager.login_view='login'

@login_manager.user_loader
def load_user(user_id):
    return models.User.query.get(int(user_id))

#Routes
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form=SignUpForm()
    if form.validate_on_submit():
        print("test1")
        if form.username.data in [user.username for user in models.User.query.all()]:
            print("test2")
            flash('Username already exists', 'danger')
        else:
            print("test3")
            new_user=models.User(username=form.username.data, password=form.password.data)
            db.session.add(new_user)
            db.session.commit() 
            flash('Account created!', 'success')
            login_user(new_user)
            return redirect(url_for('home'))
    return render_template('signup.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form=LoginForm()
    if form.validate_on_submit():
        user=models.User.query.filter_by(username=form.username.data).first()
        if user and user.password == form.password.data:
            login_user(user)
            flash('Login successful!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html', form=form)

@app.route('/')
def home():
    if current_user.is_authenticated == True:
        return render_template('home.html',
                               title="Game Review Site",
                               username=current_user.username)
    else:
        return render_template('home.html',
                            title="Game Review Site",
                            username="Guest")

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out!', 'info')
    return redirect(url_for('login'))

@app.route('/create_review', methods=['GET', 'POST'])
@login_required
def create_review():
    form=NewReview()
    games=models.Game.query.all()
    form.game.choices=[game.name for game in games]
    if form.validate_on_submit():
        if form.game.data not in [game.name for game in games]:
            flash('Game not found', 'danger')
            return redirect(url_for('create_review'))
        elif current_user.id in [review.user_id for review in models.Review.query.join(models.Game).filter_by(id=models.Game.query.filter_by(name=form.game.data).first().id).all()]:
            flash('You have already reviewed this game', 'danger')
            return redirect(url_for('create_review'))
        p = models.Review(rating=form.rating.data,
                          review=form.review.data,
                          user_id=current_user.id,
                          game_id=models.Game.query.filter_by(name=form.game.data).first().id)
        db.session.add(p)
        db.session.commit()
        return redirect(url_for('reviews', game_id=models.Game.query.filter_by(name=form.game.data).first().id))
    return render_template("create.html",
                           form=form,
                           title="Create New Review")

@app.route('/game_list', methods=['GET'])
def game_list():
    games=models.Game.query.all()
    return render_template("games.html",
                           games=games,
                           title="Games")

@app.route('/reviews/<game_id>', methods=['GET'])
@login_required
def reviews(game_id):
    reviews=models.Review.query.join(models.Game).join(models.User).filter(models.Review.game_id == game_id).all()
    game_name=models.Game.query.get(game_id).name
    return render_template("reviews.html",
                           reviews=reviews,
                           game_name=game_name,
                           user=current_user,
                           title=game_name + "Reviews")

@app.route('/like/<review_id>', methods=['GET','POST'])
@login_required
def like(review_id):
    print(f'user {current_user.id}    review {review_id}')
    review=models.Review.query.get(review_id)
    user_like = db.session.query(models.likes_table).filter_by(user_id=current_user.id, review_id=review.id).first()
    #further server side validation not needed
    #as the button checks here if the user has already liked the review
    if user_like:
        db.session.query(models.likes_table).filter_by(user_id=current_user.id, review_id=review.id).delete()
        action = "unlike"
    else:
        db.session.execute(models.likes_table.insert().values(user_id=current_user.id, review_id=review.id))
        action = "liked"

    db.session.commit()

    users = db.session.query(models.User).join(models.likes_table).filter(models.likes_table.c.review_id == review.id).all()
    likes = [user.username for user in users]
    return jsonify({"likes": likes, "action": action})