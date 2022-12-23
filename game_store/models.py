from sqlalchemy import CheckConstraint
from game_store import db, login_manager
from flask_login import UserMixin
import datetime


@login_manager.user_loader
def load_user(user_id):
    return Customer.query.get(int(user_id))


class Customer(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    balance = db.Column(db.Numeric(4, 2))
    orders = db.relationship("Purchase", cascade="all, delete-orphan")
    returns = db.relationship("Return", cascade="all, delete-orphan")
    __table_args__ = (
        CheckConstraint(balance >= 0, name='check_bar_positive'),
        {})

    def __init__(self, username, email, password, balance):
        self.username = username
        self.email = email
        self.password = password
        self.balance = balance

    def __repr__(self):
        return f"Customer('{self.username}', '{self.email}', '{self.balance}')"


class Purchase(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'))
    date = db.Column(db.DateTime, nullable=False)
    game_id = db.Column(db.Integer, db.ForeignKey('game.id'))
    qty = db.Column(db.Integer)

    def __init__(self, customer_id, date, game_id, qty):
        self.customer_id = customer_id
        self.date = date
        self.game_id = game_id
        self.qty = qty

    def __repr__(self):
        return f"Purchase('{self.customer_id}', '{self.date}', '{self.game_id}', '{self.qty}')"


class Return(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    purchase_id = db.Column(db.Integer, db.ForeignKey('purchase.id'), nullable=False)

    def __init__(self, customer_id, date, purchase_id):
        self.customer_id = customer_id
        self.date = date
        self.purchase_id = purchase_id

    def __repr__(self):
        return f"Return('{self.date}')"


class Publisher(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    publisher_name = db.Column(db.String(20), nullable=False)

    def __init__(self, publisher_name):
        self.publisher_name = publisher_name

    def __repr__(self):
        return f"Publisher('{self.publisher_name}')"


class Game(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    game_name = db.Column(db.String(50), nullable=False)
    genre = db.Column(db.String(50), nullable=False)
    release_date = db.Column(db.Date, nullable=False)
    price = db.Column(db.Numeric(4, 2), nullable=False)
    description = db.Column(db.String(200), nullable=False)
    publisher_id = db.Column(db.Integer, db.ForeignKey('publisher.id'))
    runs = db.relationship("Run", cascade="all, delete-orphan")

    def __init__(self, game_name, genre, release_date, price, description, publisher_id):
        self.game_name = game_name
        self.genre = genre
        self.release_date = release_date
        self.price = price
        self.description = description
        self.publisher_id = publisher_id

    def __repr__(self):
        return f"Game('{self.game_name}', '{self.genre}', '{self.release_date}', '{self.price}', '{self.description}', '{self.publisher_id}')"


class Platform(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    platform_name = db.Column(db.String(50), nullable=False)
    release_date = db.Column(db.Date, nullable=False)
    price = db.Column(db.Numeric(4, 2), nullable=False)
    runs = db.relationship("Run", cascade="all, delete-orphan")

    def __init__(self, platform_name, release_date, price):
        self.platform_name = platform_name
        self.release_date = release_date
        self.price = price

    def __repr__(self):
        return f"Game('{self.platform_name}', '{self.release_date}', '{self.price}')"


class Run(db.Model):
    platform_id = db.Column(db.Integer, db.ForeignKey('platform.id'), primary_key=True)
    game_id = db.Column(db.Integer, db.ForeignKey('game.id'), primary_key=True)

    def __init__(self, platform_id, game_id):
        self.platform_id = platform_id
        self.game_id = game_id

    def __repr__(self):
        return f"Run('{self.platform_id}', '{self.game_id}')"

#Game.__table__.drop(db.engine)
#Publisher.__table__.drop(db.engine)
#Platform.__table__.drop(db.engine)
#Run.__table__.drop(db.engine)
#Game.__table__.create(db.engine)
#Publisher.__table__.create(db.engine)
#Platform.__table__.create(db.engine)
#Run.__table__.create(db.engine)

db.create_all()
games = [
    Game(game_name="Assassin's Creed", genre="action-adventure", release_date=datetime.date(2007, 11, 13), price=10.00, description='The first game in the Assassins Creed franchise is set in 1191 AD, when the Third Crusade was tearing the Holy Land apart. Shrouded in secrecy and feared for their ruthlessness, the Assassins intend to stop the hostilities by suppressing both sides of the conflict. Players, assuming the role of the main character Altair, will have the power to throw their immediate environment into chaos and to shape events during this pivotal moment in history'
         ,publisher_id=1),
    Game(game_name="Assassin's Creed II", genre="action-adventure", release_date=datetime.date(2009, 11, 17),
         price=15.00, description='The second game in the Assassin’s Creed franchise which allows the player to discover an intriguing & fascinating new epic story of power, revenge and conspiracy set in a pivotal moment of History: the Italian Renaissance.' ,publisher_id=1),
    Game(game_name="Assassin's Creed III", genre="action-adventure", release_date=datetime.date(2012, 10, 30),
         price=25.00, description='The American Colonies, 1775. Its a time of civil unrest and political upheaval in the Americas. As a Native American assassin fights to protect his land and his people, he will ignite the flames of a young nations revolution.' ,publisher_id=1),
    Game(game_name="Assassin's Creed Brotherhood", genre="action-adventure", release_date=datetime.date(2010, 11, 16),
         price=15.00, description='Whether youre moving into a new apartment or fighting against the corruption of the Templar Order, its always good to have help. Master Assassin Ezio enlists the aid of the Brotherhood, an order of assassins dedicated to toppling the corrupt Templar tyrants. In order to strike at the heart of their enemy, they must journey to Rome, the center of the Templars power and greed. Assassins Creed Brotherhood features a series-first multiplayer mode that allows you to choose from a variety characters, each with unique weapons and techniques, and then match your skills against other assassins from around the world.' ,publisher_id=1),
    Game(game_name="Assassin's Creed Revelations", genre="action-adventure", release_date=datetime.date(2011, 11, 15),
         price=20.00, description='When a mans battles have been won and his enemies destroyed what then? Where does he find purpose and meaning? To find answers to these questions, Ezio Auditore will travel east in search of the lost library of the Assassins. In Assassins Creed® Revelations, master assassin Ezio Auditore walks in the footsteps of the legendary mentor Altair, on a journey of discovery and revelation. It is a perilous path - one that will take Ezio to Constantinople, the heart of the Ottoman Empire, where a growing army of Templars threatens to destabilize the region.' ,publisher_id=1),
    Game(game_name="Mass Effect 2", genre="action role-playing", release_date=datetime.date(2010, 1, 26), price=10.00, description='"Mass Effect" is a science-fiction action and role-playing game (RPG) created by BioWare, the commercially and critically acclaimed RPG developer of "Jade Empire” and "Star Wars: Knights of the Old Republic." "Mass Effect" delivers an immersive, story-driven gameplay experience with stunning visual fidelity. As one of the first human beings to step onto the galactic stage, you face a grave threat that may destroy all of civilization. Your job is complicated by the fact that no one believes that there is any threat at all. Travel across an expansive universe, exploring the uncharted corners of the galaxy, searching for pieces of the truth in order to discover how to defeat the coming destruction.' ,
         publisher_id=2),
    Game(game_name="Need for Speed", genre="racing", release_date=datetime.date(2015, 11, 3), price=25.00, description='Discover the nocturnal open world of urban car culture, driven by Five Ways to Play, in this thrilling reboot of Need for Speed. Carve your own unique path, via multiple overlapping stories, gaining reputation on your journey to become the ultimate icon. Need for Speed delivers on what fans have been requesting and what the franchise stands for - deep customization, an authentic open world filled with real world car culture, and a narrative that drives your game.',
         publisher_id=2),
    Game(game_name="Anthem", genre="action role-playing", release_date=datetime.date(2019, 2, 22), price=60.00, description='On a world left unfinished by the gods, a shadowy faction threatens all of humankind. The only thing that stands between these villains and the ancient technology they covet are the Freelancers.' ,
         publisher_id=2),
    Game(game_name="Titanfall", genre="first-person shooter", release_date=datetime.date(2014, 3, 11), price=20.00, description='Prepare for Titanfall. Crafted by one of the co-creators of Call of Duty and other key developers behind the Call of Duty franchise, Titanfall is an all-new universe juxtaposing small vs. giant, natural vs. industrial and man vs. machine. The visionaries at Respawn have drawn inspiration from their proven experiences in first-person action and with Titanfall are focused on bringing something exciting to the next generation of multiplayer gaming.' ,
         publisher_id=2),
    Game(game_name="Battlefield 4", genre="first-person shooter", release_date=datetime.date(2013, 10, 29), price=15.00, description='Battlefield 4 is the genre-defining action blockbuster made from moments that blur the line between game and glory. Fueled by the next-generation power and fidelity of Frostbite 3, Battlefield 4 provides a visceral, dramatic experience unlike any other. Only in Battlefield will you blow the foundations of a dam or reduce an entire skyscraper to rubble. Only in Battlefield will you lead a naval assault from the back of a gun boat. Battlefield grants you the freedom to do more and be more while playing to your strengths and carving your own path to victory.' ,
         publisher_id=2),
    Game(game_name="Call of Duty World at War", genre="first-person shooter", release_date=datetime.date(2008, 11, 11),
         price=5.00, description='Call of Duty® delivers the gritty realism and cinematic intensity of World War IIs epic battlefield moments like never before - through the eyes of citizen soldiers and unsung heroes from an alliance of countries who together helped shape the course of modern history.' ,publisher_id=3),
    Game(game_name="Destiny", genre="first-person shooter", release_date=datetime.date(2014, 9, 9), price=20.00, description='Everything changed with the arrival of the Traveler. It sparked a Golden Age when our civilization spanned our solar system, but it didnt last. Something hit us, knocked us down. The survivors built a city beneath the Traveler, and have begun to explore our old worlds, only to find them filled with deadly foes. You are a Guardian of the last safe city on Earth, able to wield incredible power. Defend the City. Defeat our enemies. Reclaim all that we have lost. Be brave.' ,
         publisher_id=3),
    Game(game_name="Call of Duty Black Ops 4", genre="first-person shooter", release_date=datetime.date(2018, 10, 12),
         price=50.00, description='Black Ops is back! Featuring gritty, grounded Multiplayer combat, the biggest Zombies offering ever with three full undead adventures at launch, and Blackout, where the universe of Black Ops comes to life in a massive battle royale experience. Blackout features the largest map in Call of Duty history, signature Black Ops combat, and characters, locations and weapons from the Black Ops series.' ,publisher_id=3),
    Game(game_name="Crash Bandicoot", genre="platform", release_date=datetime.date(2017, 6, 30), price=40.00, description='Your favorite marsupial, Crash Bandicoot, is back! Hes enhanced, entranced & ready-to-dance with the N. Sane Trilogy game collection. Now you can experience Crash Bandicoot like never before in Fur-K. Spin, jump, wump and repeat as you take on the epic challenges and adventures through the three games that started it all, Crash Bandicoot, Crash Bandicoot 2: Cortex Strikes Back and Crash Bandicoot 3: Warped. Relive all your favorite Crash moments in their fully-remastered HD graphical glory and get ready to put some UMPH in your WUMP!' ,
         publisher_id=3),
    Game(game_name="Tony Hawk's Pro Skater", genre="sports", release_date=datetime.date(1999, 7, 31), price=2.00, description='Go Big, Go Pro! Skate as legendary Tony Hawk, or as one of nine top pros. Work your way up the ranks by landing suicidal tricks in brutal competitions to become the highest ranked skate champ! Great features such as: Signature Pro Moves, fully skateable worlds, head-to-head competition, and Instant Replay Mode.' ,
         publisher_id=3),
    Game(game_name="Bloodborne", genre="action role-playing", release_date=datetime.date(2015, 3, 24), price=30.00, description='Introducing Bloodborne, the latest Action RPG from renowned Japanese developer FromSoftware, exclusively for the PlayStation®4 system. Face your fears as you search for answers in the ancient city of Yharnam, now cursed with a strange endemic illness spreading through the streets like wildfire. Danger, death and madness lurk around every corner of this dark and horrific world, and you must discover its darkest secrets in order to survive.' ,
         publisher_id=4),
    Game(game_name="God of War", genre="action-adventure", release_date=datetime.date(2018, 4, 20), price=60.00, description='It is a new beginning for Kratos. Living as a man outside the shadow of the gods, he ventures into the brutal Norse wilds with his son Atreus, fighting to fulfill a deeply personal quest.' ,
         publisher_id=4),
    Game(game_name="The Last of Us", genre="action-adventure", release_date=datetime.date(2014, 7, 29), price=20.00, description='Winner of over 200 Game of the Year awards, The Last of Us has been rebuilt for the PlayStation®4 system. Now featuring full 1080p, higher resolution character models, improved shadows and lighting, in addition to several other gameplay improvements. 20 years after a pandemic has radically changed known civilization, infected humans run wild and survivors are killing each other for food, weapons; whatever they can get their hands on. Joel, a violent survivor, is hired to smuggle a 14 year-old girl, Ellie, out of an oppressive military quarantine zone, but what starts as a small job soon transforms into a brutal journey across the U.S. The Last of Us Remastered includes the Abandoned Territories Map Pack, Reclaimed Territories Map Pack, and the critically acclaimed The Last of Us: Left Behind Single Player campaign that combines themes of survival, loyalty, and love with tense, survival-action gameplay.' ,
         publisher_id=4),
    Game(game_name="Ratchet and Clank", genre="platform", release_date=datetime.date(2016, 4, 12), price=40.00, description='Play the game, based on the movie, based on the game! Ratchet & Clank (PS4) is a new game based on elements from the original Ratchet & Clank (PS2). Developed alongside the major motion CG-animated picture coming to theatres in 2016, Ratchet & Clank (PS4) marks the PlayStation 4 debut of PlayStations greatest heroes. Join Ratchet, Clank, Captain Qwark and new friends as they battle to save the Solana Galaxy from the evil Chairman Drek.' ,
         publisher_id=4),
    Game(game_name="Infamous Second Son", genre="action-adventure", release_date=datetime.date(2014, 3, 21),
         price=20.00, description='inFAMOUS Second Son, a PlayStation 4 exclusive , brings you an action adventure game where surrounded by a society that fears them, superhumans are ruthlessly hunted down and caged by the Department of Unified Protection. When Delsin Rowe discovers his powers hes forced to run, searching for other superhumans in order to save those he loves from the oppressive D.U.P. The actions he takes along the way will change the future of everyone around him.' ,publisher_id=4),
    Game(game_name="The Legend of Zelda: Breath of the Wild", genre="action-adventure",
         release_date=datetime.date(2017, 3, 3), price=50.00, description='Forget everything you know about The Legend of Zelda games. Step into a world of discovery, exploration, and adventure in The Legend of Zelda: Breath of the Wild, a boundary-breaking new game in the acclaimed series. Travel across vast fields, through forests, and to mountain peaks as you discover what has become of the kingdom of Hyrule In this stunning Open-Air Adventure. Now on Nintendo Switch, your journey is freer and more open than ever. Take your system anywhere, and adventure as Link any way you like.' ,publisher_id=5),
    Game(game_name="Super Mario Odyssey", genre="platform", release_date=datetime.date(2017, 10, 27), price=50.00, description='Explore incredible places far from the Mushroom Kingdom as you join Mario and his new ally Cappy on a massive, globe-trotting 3D adventure.' ,
         publisher_id=5),
    Game(game_name="Super Smash Bros. Ultimate", genre="fighting", release_date=datetime.date(2018, 12, 7), price=60.00,
         description='Gaming icons clash in the ultimate brawl you can play anytime, anywhere! Smash rivals off the stage as new characters Simon Belmont and King K. Rool join Inkling, Ridley, and every fighter in Super Smash Bros. history. Enjoy enhanced speed and combat at new stages based on the Castlevania series, Super Mario Odyssey, and more!',publisher_id=5),
    Game(game_name="Splatoon 2", genre="third-person shooter", release_date=datetime.date(2017, 7, 21), price=50.00,
         description='Ink-splatting action is back and fresher than ever. Get hyped for the sequel to the hit game about splatting ink and claiming turf, as the squid-like Inklings return in a colorful and chaotic 4 vs. 4 action shooter. For the first time, take Turf War battles on-the-go via local multiplayer in portable play styles. You can also compete in frenetic online matches like before. Two years have passed since the release of Splatoon, and two years have also passed in the game world, leading to an evolution in fashion trends and new styles of weapons and gear. Staying fresh never looked so good.',publisher_id=5),
    Game(game_name="Animal Crossing: New Leaf", genre="social simulation", release_date=datetime.date(2012, 11, 8),
         price=15.00, description='Animal Crossing: New Leaf is loaded with new characters, items, and activities to enjoy all year long. Customize outfits in countless ways. Furnish your house with an extensive variety of furniture, carpet, and wall decorations to reflect your personality. Visit the new Main Street shopping area and Happy Home Showcase. Swim in the ocean to find rare shellfish. Collect insects and fossils all year long. As mayor, make the big decisions about what to build, business hours for shops, and other new ways to customize your town to your liking. Then connect with friends to show off what makes your character, your house, and your town unique.' ,publisher_id=5)
]

db.session.bulk_save_objects(games)
db.session.commit()

publishers = [
    Publisher(publisher_name="Ubisoft"),
    Publisher(publisher_name="EA"),
    Publisher(publisher_name="Activision"),
    Publisher(publisher_name="Sony"),
    Publisher(publisher_name="Nintendo")
]

db.session.bulk_save_objects(publishers)
db.session.commit()

platforms = [
    Platform(platform_name="Playstation 2", release_date=datetime.date(2000, 10, 26), price=30.00),
    Platform(platform_name="Xbox", release_date=datetime.date(2001, 11, 15), price=30.00),
    Platform(platform_name="Nintendo Gamecube", release_date=datetime.date(2001, 11, 18), price=60.00),
    Platform(platform_name="Sega Dreamcast", release_date=datetime.date(1999, 9, 9), price=50.00),
    Platform(platform_name="Playstation", release_date=datetime.date(1995, 9, 9), price=50.00),
    Platform(platform_name="Nintendo 64", release_date=datetime.date(1996, 9, 26), price=60.00),
    Platform(platform_name="Xbox 360", release_date=datetime.date(2005, 11, 22), price=70.00),
    Platform(platform_name="Playstation 3", release_date=datetime.date(2006, 11, 17), price=80.00),
    Platform(platform_name="Nintendo Wii", release_date=datetime.date(2006, 11, 19), price=50.00),
    Platform(platform_name="Nintendo Wii U", release_date=datetime.date(2012, 11, 18), price=40.00),
    Platform(platform_name="Xbox One", release_date=datetime.date(2013, 11, 22), price=200.00),
    Platform(platform_name="Playstation 4", release_date=datetime.date(2015, 11, 15), price=250.00),
    Platform(platform_name="Nintendo Switch", release_date=datetime.date(2017, 3, 3), price=300.00),
    Platform(platform_name="Nintendo 3DS", release_date=datetime.date(2011, 3, 27), price=70.00)
]

db.session.bulk_save_objects(platforms)
db.session.commit()

runs = [
    Run(platform_id=7, game_id=1),
    Run(platform_id=8, game_id=1),
    Run(platform_id=7, game_id=2),
    Run(platform_id=8, game_id=2),
    Run(platform_id=11, game_id=2),
    Run(platform_id=12, game_id=2),
    Run(platform_id=7, game_id=3),
    Run(platform_id=8, game_id=3),
    Run(platform_id=11, game_id=3),
    Run(platform_id=12, game_id=3),
    Run(platform_id=10, game_id=3),
    Run(platform_id=13, game_id=3),
    Run(platform_id=7, game_id=4),
    Run(platform_id=8, game_id=4),
    Run(platform_id=11, game_id=4),
    Run(platform_id=12, game_id=4),
    Run(platform_id=7, game_id=5),
    Run(platform_id=8, game_id=5),
    Run(platform_id=11, game_id=5),
    Run(platform_id=12, game_id=5),
    Run(platform_id=7, game_id=6),
    Run(platform_id=8, game_id=6),
    Run(platform_id=11, game_id=7),
    Run(platform_id=12, game_id=7),
    Run(platform_id=11, game_id=8),
    Run(platform_id=12, game_id=8),
    Run(platform_id=11, game_id=9),
    Run(platform_id=7, game_id=9),
    Run(platform_id=7, game_id=10),
    Run(platform_id=8, game_id=10),
    Run(platform_id=11, game_id=10),
    Run(platform_id=12, game_id=10),
    Run(platform_id=7, game_id=11),
    Run(platform_id=8, game_id=11),
    Run(platform_id=9, game_id=11),
    Run(platform_id=7, game_id=12),
    Run(platform_id=8, game_id=12),
    Run(platform_id=11, game_id=12),
    Run(platform_id=12, game_id=12),
    Run(platform_id=11, game_id=13),
    Run(platform_id=12, game_id=13),
    Run(platform_id=11, game_id=14),
    Run(platform_id=12, game_id=14),
    Run(platform_id=13, game_id=14),
    Run(platform_id=4, game_id=15),
    Run(platform_id=5, game_id=15),
    Run(platform_id=6, game_id=15),
    Run(platform_id=12, game_id=16),
    Run(platform_id=12, game_id=17),
    Run(platform_id=8, game_id=18),
    Run(platform_id=8, game_id=19),
    Run(platform_id=8, game_id=20),
    Run(platform_id=13, game_id=21),
    Run(platform_id=10, game_id=21),
    Run(platform_id=13, game_id=22),
    Run(platform_id=13, game_id=23),
    Run(platform_id=13, game_id=24),
    Run(platform_id=14, game_id=25),
]
#db.session.bulk_save_objects(runs)
#db.session.commit()

