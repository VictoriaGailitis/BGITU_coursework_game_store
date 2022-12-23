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
    publishers = Publisher.query.all()
    games = Game.query.all()
    return render_template('home.html', games=games, publishers=publishers)


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
        this_purchase = Purchase(customer_id=current_user.id, date=datetime.datetime.now(), game_id=buying_game.id, qty=form.quantity.data)
        db.session.add(this_purchase)
        # db.session.commit()
        # flash('your purchase was successful')
        # return redirect(url_for('account'))
        try:
            db.session.commit()
            flash('Your purchase for ' + str(total_price) + ' was successful', 'success')
            return redirect(url_for('account'))
        except:
            db.session.rollback()
            flash('You do not have enough money for this purchase!', 'warning')

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
        flash('Your account has been created! You are now able to log in', 'success')
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
            flash('Login Unsuccessful. Please check email and password', 'danger')
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


@app.route("/genres")
def genre():
    return render_template('genres.html')

@app.route("/publisher")
def publish():
    return render_template('publisher.html')

@app.route("/platforms")
def platform():
    return render_template('platforms.html')

@app.route('/aa')
def actionadv():
    publishers = Publisher.query.all()
    games = Game.query.filter_by(genre = 'action-adventure').all()
    return render_template('gamelist.html', games=games, publishers=publishers)

@app.route('/ps2')
def ps2():
    runs = Run.query.filter_by(platform_id = 1).all()
    #platforms = Platform.query.filter_by(12).all()
    publishers = Publisher.query.all()
    games = Game.query.filter(Game.runs.any(platform_id=1))
    return render_template('gamelist.html', games=games, publishers=publishers, run=runs)

@app.route('/xb')
def xb():
    runs = Run.query.filter_by(platform_id = 2).all()
    #platforms = Platform.query.filter_by(12).all()
    publishers = Publisher.query.all()
    games = Game.query.filter(Game.runs.any(platform_id=2))
    return render_template('gamelist.html', games=games, publishers=publishers, run=runs)

@app.route('/gc')
def gc():
    runs = Run.query.filter_by(platform_id = 3).all()
    #platforms = Platform.query.filter_by(12).all()
    publishers = Publisher.query.all()
    games = Game.query.filter(Game.runs.any(platform_id=3))
    return render_template('gamelist.html', games=games, publishers=publishers, run=runs)

@app.route('/dc')
def dc():
    runs = Run.query.filter_by(platform_id = 4).all()
    #platforms = Platform.query.filter_by(12).all()
    publishers = Publisher.query.all()
    games = Game.query.filter(Game.runs.any(platform_id=4))
    return render_template('gamelist.html', games=games, publishers=publishers, run=runs)

@app.route('/ps')
def ps():
    runs = Run.query.filter_by(platform_id = 5).all()
    #platforms = Platform.query.filter_by(12).all()
    publishers = Publisher.query.all()
    games = Game.query.filter(Game.runs.any(platform_id=5))
    flash("Games that are on the Playstation")
    return render_template('gamelist.html', games=games, publishers=publishers, run=runs)

@app.route('/n64')
def n64():
    runs = Run.query.filter_by(platform_id = 6).all()
    #platforms = Platform.query.filter_by(12).all()
    publishers = Publisher.query.all()
    games = Game.query.filter(Game.runs.any(platform_id=6))
    flash("Games that are on the Nintendo 64")
    return render_template('gamelist.html', games=games, publishers=publishers, run=runs)

@app.route('/x360')
def x360():
    runs = Run.query.filter_by(platform_id = 7).all()
    #platforms = Platform.query.filter_by(12).all()
    publishers = Publisher.query.all()
    games = Game.query.filter(Game.runs.any(platform_id=7))
    return render_template('gamelist.html', games=games, publishers=publishers, run=runs)

@app.route('/ps3')
def ps3():
    runs = Run.query.filter_by(platform_id = 8).all()
    #platforms = Platform.query.filter_by(12).all()
    publishers = Publisher.query.all()
    games = Game.query.filter(Game.runs.any(platform_id=8))
    return render_template('gamelist.html', games=games, publishers=publishers, run=runs)

@app.route('/wii')
def wii():
    runs = Run.query.filter_by(platform_id = 9).all()
    #platforms = Platform.query.filter_by(12).all()
    publishers = Publisher.query.all()
    games = Game.query.filter(Game.runs.any(platform_id=9))
    flash("Games that are on the Nintendo Wii")
    return render_template('gamelist.html', games=games, publishers=publishers, run=runs)

@app.route('/wiiu')
def wiiu():
    runs = Run.query.filter_by(platform_id = 10).all()
    #platforms = Platform.query.filter_by(12).all()
    publishers = Publisher.query.all()
    games = Game.query.filter(Game.runs.any(platform_id=10))
    flash("Games that are on the Nintendo Wii-U")
    return render_template('gamelist.html', games=games, publishers=publishers, run=runs)

@app.route('/xone')
def xone():
    runs = Run.query.filter_by(platform_id = 11).all()
    #platforms = Platform.query.filter_by(12).all()
    publishers = Publisher.query.all()
    games = Game.query.filter(Game.runs.any(platform_id=11))
    return render_template('gamelist.html', games=games, publishers=publishers, run=runs)

@app.route('/ps4')
def ps4():
    runs = Run.query.filter_by(platform_id = 12).all()
    #platforms = Platform.query.filter_by(12).all()
    publishers = Publisher.query.all()
    games = Game.query.filter(Game.runs.any(platform_id=12))
    return render_template('gamelist.html', games=games, publishers=publishers, run=runs)

@app.route('/switch')
def switch():
    runs = Run.query.filter_by(platform_id=13).all()
    #platforms = Platform.query.filter_by(12).all()
    publishers = Publisher.query.all()
    games = Game.query.filter(Game.runs.any(platform_id=13))
    flash("Games that are on the Nintendo Switch")
    return render_template('gamelist.html', games=games, publishers=publishers, run=runs)

@app.route('/3ds')
def n3ds():
    runs = Run.query.filter_by(platform_id = 14).all()
    #platforms = Platform.query.filter_by(12).all()
    publishers = Publisher.query.all()
    games = Game.query.filter(Game.runs.any(platform_id=14))
    flash("Games that are on the Nintendo 3ds")
    return render_template('gamelist.html', games=games, publishers=publishers, run=runs)

@app.route('/arp')
def arp():
    publishers = Publisher.query.all()
    games = Game.query.filter_by(genre='action role-playing').all()
    return render_template('gamelist.html', games=games, publishers=publishers)

@app.route('/fps')
def fps():
    publishers = Publisher.query.all()
    games = Game.query.filter_by(genre='first-person shooter').all()
    return render_template('gamelist.html', games=games, publishers=publishers)

@app.route('/platform')
def plat():
    publishers = Publisher.query.all()
    games = Game.query.filter_by(genre='platform').all()
    return render_template('gamelist.html', games=games, publishers=publishers)

@app.route('/sports')
def sports():
    publishers = Publisher.query.all()
    games = Game.query.filter_by(genre='sports').all()
    return render_template('gamelist.html', games=games, publishers=publishers)

@app.route('/fight')
def fight():
    publishers = Publisher.query.all()
    games = Game.query.filter_by(genre='fighting').all()
    return render_template('gamelist.html', games=games, publishers=publishers)

@app.route('/tps')
def tps():
    publishers = Publisher.query.all()
    games = Game.query.filter_by(genre='third-person shooter').all()
    return render_template('gamelist.html', games=games, publishers=publishers)

@app.route('/social')
def social():
    publishers = Publisher.query.all()
    games = Game.query.filter_by(genre='social simulation').all()
    return render_template('gamelist.html', games=games, publishers=publishers)

@app.route("/ubisoft")
def ubisoft():
    publishers = Publisher.query.all()
    games = Game.query.filter_by(publisher_id=1).all()
    return render_template('gamelist.html', games=games, publishers=publishers)

@app.route("/ea")
def ea():
    publishers = Publisher.query.all()
    games = Game.query.filter_by(publisher_id=2).all()
    return render_template('gamelist.html', games=games, publishers=publishers)

@app.route("/sony")
def sony():
    publishers = Publisher.query.all()
    games = Game.query.filter_by(publisher_id=4).all()
    return render_template('gamelist.html', games=games, publishers=publishers)

@app.route("/nintendo")
def nintendo():
    publishers = Publisher.query.all()
    games = Game.query.filter_by(publisher_id=5).all()
    return render_template('gamelist.html', games=games, publishers=publishers)

@app.route("/activision")
def activision():
    publishers = Publisher.query.all()
    games = Game.query.filter_by(publisher_id=3).all()
    return render_template('gamelist.html', games=games, publishers=publishers)

