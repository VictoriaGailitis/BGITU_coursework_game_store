from flask import render_template, url_for, flash, redirect, request
from game_store import app, db, bcrypt
from game_store.forms import RegistrationForm, LoginForm, BuyForm, ReturnForm, AddMoneyForm
from game_store.models import Customer, Purchase, Return
from flask_login import login_user, current_user, logout_user, login_required
from game_store.models import Game, Publisher, Run, Platform
import datetime


@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html')


@app.route("/about")
def about():
    return render_template('about.html', title='About')


@app.route("/gamelist")
def gl():
    publishers = Publisher.query.all()
    games = Game.query.all()

    return render_template('gamelist.html', games=games, publishers=publishers)


@app.route("/game/<selected_game>", methods=['GET', 'POST'])
@login_required
def game(selected_game):
    form = BuyForm()
    if form.validate_on_submit():
        game_name = selected_game
        buying_game = Game.query.filter_by(game_name=game_name).first()
        total_price = form.quantity.data * buying_game.price
        current_user.balance -= total_price
        this_purchase = Purchase(customer_id=current_user.id, date=datetime.datetime.now(), game_id=buying_game.id,
                                 qty=form.quantity.data)
        db.session.add(this_purchase)
        # db.session.commit()
        # flash('your purchase was successful')
        # return redirect(url_for('account'))
        try:
            db.session.commit()
            flash('Покупка ' + str(total_price) + ' прошла успешно', 'success')
            return redirect(url_for('account'))
        except:
            db.session.rollback()
            flash('У Вас не хватает денег на счету для этой покупки!', 'warning')

    return render_template('game.html', game=selected_game, form=form, title='Game')


@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = Customer(username=form.username.data, email=form.email.data, password=hashed_password, balance=40.00)
        db.session.add(user)
        db.session.commit()
        flash('Аккаунт создан! Теперь возможен вход', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = Customer.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Ошибка входа. Проверьте логин и пароль', 'danger')
    return render_template('login.html', title='Login', form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = AddMoneyForm()
    if form.validate_on_submit():
        current_user.balance += 20
        db.session.commit()
        return redirect(url_for('account'))

    orders = Purchase.query.all()
    games = Game.query.all()
    returns = Return.query.all()
    return render_template('account.html', orders=orders, games=games, returns=returns, form=form)

@app.route("/returns/<selected_purchase>", methods=['GET', 'POST'])
def returns(selected_purchase):
    form = ReturnForm()
    purchase = Purchase.query.filter_by(id=selected_purchase).first()
    purchased_game_id = purchase.game_id
    purchased_game = Game.query.filter_by(id=purchased_game_id).first()
    total_spent = purchased_game.price * purchase.qty

    if form.validate_on_submit():
        thereturn = Return(current_user.id, datetime.datetime.now(), selected_purchase)
        db.session.add(thereturn)
        current_user.balance += total_spent
        db.session.commit()
        return redirect(url_for('account'))

    return render_template('returns.html', form=form, title='Returns')

@app.route("/publisher")
def publish():
    publishers = Publisher.query.all()
    return render_template('publisher.html', publishers=publishers)

@app.route('/show_publisher/<selected_publisher>')
def selected_publisher(selected_publisher):
    publishers = Publisher.query.all()
    games = Game.query.filter_by(publisher_id=selected_publisher)
    return render_template('gamelist.html', games=games, publishers=publishers)

@app.route("/platforms")
def platform():
    platforms = Platform.query.all()
    return render_template('platforms.html', platforms=platforms)

@app.route('/show_platform/<selected_platform>')
def selected_platform(selected_platform):
    runs = Run.query.filter_by(platform_id = selected_platform).all()
    publishers = Publisher.query.all()
    games = Game.query.filter(Game.runs.any(platform_id=selected_platform))
    return render_template('gamelist.html', games=games, publishers=publishers, run=runs)

@app.route("/genres")
def genre():
    games = db.session.query(Game).distinct(Game.genre).group_by(Game.genre)
    return render_template('genres.html', games=games)

@app.route('/show_genre/<selected_genre>')
def selected_genre(selected_genre):
    games = Game.query.filter_by(genre=selected_genre)
    return render_template('gamelist.html', games=games)


