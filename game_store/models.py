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
    poster = db.Column(db.String(100), nullable=False)
    runs = db.relationship("Run", cascade="all, delete-orphan")

    def __init__(self, game_name, genre, release_date, price, description, publisher_id, poster):
        self.game_name = game_name
        self.genre = genre
        self.release_date = release_date
        self.price = price
        self.description = description
        self.publisher_id = publisher_id
        self.poster = poster

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

#db.create_all()

games = [
    Game(game_name="Assassin's Creed", genre="action-adventure", release_date=datetime.date(2007, 11, 13), price=10.00,
         description='Ваш персонаж - ассасин, таинственный воин, не ведающий пощады. Своими действиями вы способны'
                     ' устроить настоящий хаос. Именно вы определяете события поворотных периодов истории.'
         ,publisher_id=1, poster="https://static.wikia.nocookie.net/assassinscreed/images/6/6a/Accover.jpg/revision"
                                 "/latest?cb=20161203080803&path-prefix=ru"),
    Game(game_name="Assassin's Creed II", genre="action-adventure", release_date=datetime.date(2009, 11, 17),
         price=15.00, description='Интриги и месть в захватывающей истории одного рода в чарующем, но жестоком антураже'
                                  ' Италии эпохи Возрождения.' ,publisher_id=1,
         poster="https://upload.wikimedia.org/wikipedia/en/7/77/Assassins_Creed_2_Box_Art.JPG"),
    Game(game_name="Assassin's Creed III", genre="action-adventure", release_date=datetime.date(2012, 10, 30),
         price=25.00, description='Переживите события Американской революции заново в обновлённой версии Assassins'
                                  'Creed® III Remastered с улучшенными графикой и игровой механикой. В комплект входят'
                                  'все дополнения для одиночной игры и обновлённая версия Assassins Creed Liberation.'
         ,publisher_id=1, poster="https://upload.wikimedia.org/wikipedia/en/2/29/Assassin%27s_Creed_III_Game_Cover.jpg"),
    Game(game_name="Assassin's Creed Brotherhood", genre="action-adventure", release_date=datetime.date(2010, 11, 16),
         price=15.00, description='Эцио Аудиторре удалось отомстить за убийство своего отца и братьев. Поднявшись на'
                                  ' вершину иерархии ордена Ассасинов, он решает уйти на покой и провести оставшиеся'
                                  ' годы жизни в тишине и покое. Но трагические обстоятельства вынуждает Эцио вернуться'
                                  ' в Рим, чтобы освободить город от коррумпированного правительства, нищеты и заговора'
                                  ' Тамплиеров.' ,publisher_id=1,
         poster="https://upload.wikimedia.org/wikipedia/en/2/2a/Assassins_Creed_brotherhood_cover.jpg"),
    Game(game_name="Assassin's Creed Revelations", genre="action-adventure", release_date=datetime.date(2011, 11, 15),
         price=20.00, description='Разве постаревший Ассасин не заслуживает пенсию, отдых в семейной вилле и других'
                                  ' прелестей жизни? Но Эцио Аудиторре решает, что всё это уже не для него. Все враги'
                                  ' повержены, а войны выиграны. Пришло время достичь чего-то большего. Прославившийся'
                                  ' мастер-ассасин отправляется в своё последнее и самое опасное приключение на Восток.'
                                  ' Он намерен пройти по пути Альтаира, чтобы познать всю истину бытия.' ,publisher_id=1,
         poster="https://upload.wikimedia.org/wikipedia/en/d/d9/Assassins_Creed_Revelations_Cover.jpg"),
    Game(game_name="Mass Effect 2", genre="action role-playing", release_date=datetime.date(2010, 1, 26), price=10.00,
         description='От создателей Star Wars: Knights of the Old Republic, Dragon Age: Origins и Mass Effect встречайте'
                     ' второй тёмный эпизод эпичной трилогии Mass Effect.Через два года после того, как капитан Шепард'
                     ' отразил вторжение Жнецов, стремившихся уничтожить всю органическую жизнь во вселенной, у'
                     ' человечества появился новый враг.' ,
         publisher_id=2, poster="https://upload.wikimedia.org/wikipedia/en/0/05/MassEffect2_cover.PNG"),
    Game(game_name="Need for Speed", genre="racing", release_date=datetime.date(2015, 11, 3), price=25.00,
         description='Популярнейшая и всемирно известная серия гоночных игр Need For Speed развивается и пахнет свежей'
                     ' краской, новым салоном и бензином. Студия Ghost Games смело взяла на себя ответственность за'
                     ' перезапуск NFS, делая из старого, нечто новое! Около двух лет они изучали нужды аудитории, они'
                     ' хотели вдохнуть в этот жанр свежего глотка воздуха! Учли множество аспектов, поняли, чего хотят'
                     ' поклонники и добились желаемого!',
         publisher_id=2, poster="https://upload.wikimedia.org/wikipedia/en/a/a9/Need_for_Speed_2015.jpg"),
    Game(game_name="Anthem", genre="action role-playing", release_date=datetime.date(2019, 2, 22), price=60.00,
         description='Вы попадете в мир, в котором сплелились воедино тонкая энергия, высокие технологии и дикая'
                     'природа. В роли фрилансера - пилота боевого джавелина, - вам предстоит выяснить причину'
                     'катаклизмов и разобраться с коварными врагами, которые замыслили подчинить себе энергию творения.' ,
         publisher_id=2, poster="https://upload.wikimedia.org/wikipedia/en/4/49/Cover_Art_of_Anthem.jpg"),
    Game(game_name="Titanfall", genre="first-person shooter", release_date=datetime.date(2014, 3, 11), price=20.00,
         description='Titanfall — это экшен с видом от первого лица с элементами шутера и симулятора роботов от'
                     'мастеров из студий Bluepoint Games, Inc. и Respawn Entertainment.' ,
         publisher_id=2, poster="https://upload.wikimedia.org/wikipedia/en/8/84/Titanfall_box_art.jpg"),
    Game(game_name="Battlefield 4", genre="first-person shooter", release_date=datetime.date(2013, 10, 29), price=15.00,
         description='6 лет прошло после событий Battlefield 3, и вот наступил 2020 год. Игроку предстоит примерить на'
                     'себя роль разведчика Дэниела Рекера, сержанта разведывательного отряда, именующегося группой'
                     '«Tombstone». Подразделению дали задачу прибыть в Баку и выведать особо важное информорфирование от'
                     'русского генерала в бегах. Неожиданно группу раскрывают и бойцам ничего не остается, кроме как'
                     'пробираться назад, борясь с превосходящей по силе российской армией.' ,
         publisher_id=2, poster="https://upload.wikimedia.org/wikipedia/en/7/75/Battlefield_4_cover_art.jpg"),
    Game(game_name="Call of Duty World at War", genre="first-person shooter", release_date=datetime.date(2008, 11, 11),
         price=5.00, description='Потрясающий шутер от первого лица, действия в котором происходят во время Второй'
                                 'мировой войны. Сюжет не заставит вас скучать: 15 различных миссий с переменной сменой'
                                 'вашего персонажа. Отличная графика и геймплей, удобное управление.' ,publisher_id=3,
         poster="https://upload.wikimedia.org/wikipedia/en/1/19/Call_of_Duty_World_at_War_cover.png"),
    Game(game_name="Destiny", genre="first-person shooter", release_date=datetime.date(2014, 9, 9), price=20.00,
         description='Destiny 2 – это экшен-MMO в едином развивающемся мире, к которому вы с друзьями можете'
                     'присоединиться где и когда угодно, абсолютно бесплатно.' ,
         publisher_id=3, poster="https://upload.wikimedia.org/wikipedia/en/0/06/Destiny_XBO.jpg"),
    Game(game_name="Call of Duty Black Ops 4", genre="first-person shooter", release_date=datetime.date(2018, 10, 12),
         price=50.00, description='Call of Duty®: Black Ops 4 – это суровая, жесткая и динамичная сетевая игра, целых'
                                  ' три приключения с мертвецами в режиме “Зомби”, и режим “Затмение”, где вселенная'
                                  ' Black Ops воплотится в грандиозной “королевской битве”. Black Ops 4 будет самой'
                                  ' внушительной, безупречной и масштабируемой игрой Call of Duty® для PC в истории.'
                                  ' Вас ждет неограниченная частота кадров, разрешение 4К, HDR, поддержка сверхшироких'
                                  ' мониторов и множество других функций, ориентированных на пользователей '
                                  ' компьютеров.' ,publisher_id=3,
         poster="https://upload.wikimedia.org/wikipedia/en/1/1c/Call_of_Duty_Black_Ops_4_official_box_art.jpg"),
    Game(game_name="Crash Bandicoot", genre="platform", release_date=datetime.date(2017, 6, 30), price=40.00,
         description='Всеобщий сумчатый любимец Crash Bandicoot™ возвращается! В коллекции N. Sane Trilogy он стал еще'
                     ' шустрее, веселее и обаятельнее! Переживите заново любимые моменты игр Crash Bandicoot™,'
                     'Crash Bandicoot™ 2: Cortex Strikes Back и Crash Bandicoot™ 3: Warped, увидев их во всем блеске'
                     'полностью переработанной графики!' ,
         publisher_id=3,
         poster="https://upload.wikimedia.org/wikipedia/en/d/de/Crash_Bandicoot_N._Sane_Trilogy_cover_art.jpg"),
    Game(game_name="Tony Hawk's Pro Skater", genre="sports", release_date=datetime.date(1999, 7, 31), price=2.00,
         description='Снова прокатитесь с ветерком в самом легендарном симуляторе скейтбординга. Играйте за легендарного'
                     'Тони Хоука и других профи из оригинальной игры, а также за новых звёзд скейтбординга. Кайфуйте'
                     'под ностальгическую музыку, а также новые треки. Мочите мощные комбо, используя классическое'
                     'управление серии Tony Hawks™ Pro Skater™. Все оригинальные режимы игры и не только. Играйте во'
                     'всех оригинальных режимах и один на один в режимах для двух игроков. Демонстрируйте свой стиль и'
                     'творчество в улучшенных режимах создания парка (Create-A-Park) и скейтера (Create-A-Skater).'
                     'Соревнуйтесь с игроками со всего мира в многопользовательских режимах и в таблицах лидеров.' ,
         publisher_id=3, poster="https://upload.wikimedia.org/wikipedia/en/5/58/TonyHawksProSkaterPlayStation1.jpg"),
    Game(game_name="Bloodborne", genre="action role-playing", release_date=datetime.date(2015, 3, 24), price=30.00,
         description='Одинокий путник. Проклятый город. Смертоносная тайна, уничтожающая все, к чему она прикоснется.'
                     'Взгляните в лицо своим страхам на улицах загнивающего Ярнама — проклятого места, разъедаемого'
                     'ужасным, всепоглощающим мором. Доживете ли до рассвета?' ,
         publisher_id=4, poster="https://upload.wikimedia.org/wikipedia/en/6/68/Bloodborne_Cover_Wallpaper.jpg"),
    Game(game_name="God of War", genre="action-adventure", release_date=datetime.date(2018, 4, 20), price=60.00,
         description='Отомстив богам Олимпа, Кратос поселился в царстве скандинавских божеств и чудовищ. В этом суровом'
                     'беспощадном мире он должен не только самостоятельно бороться за выживание... но и научить этому'
                     'сына.' ,
         publisher_id=4, poster="https://upload.wikimedia.org/wikipedia/en/a/a7/God_of_War_4_cover.jpg"),
    Game(game_name="The Last of Us", genre="action-adventure", release_date=datetime.date(2014, 7, 29), price=20.00,
         description='Игра The Last of Us™ с эмоциональным сюжетом и незабываемыми персонажами получила более 200'
                     'наград «Игра года». Цивилизации настал конец, беснуются заражённые выжившие, а Джоэлу, усталому'
                     'главному герою, поручено вывести 14-летнюю Элли из военной карантинной зоны. Лёгкая, казалось бы,'
                     'задача превращается в тяжкий путь через всю страну.' ,
         publisher_id=4, poster="https://upload.wikimedia.org/wikipedia/en/4/46/Video_Game_Cover_-_The_Last_of_Us.jpg"),
    Game(game_name="Ratchet and Clank", genre="platform", release_date=datetime.date(2016, 4, 12), price=40.00,
         description='Будь вы давним поклонником Рэтчета или новичком в этой серии игр, приготовьтесь к незабываемому'
                     'путешествию по вселенной в их первом космическом приключении, полностью переосмысленном и'
                     'переизданном для PS4™. Вас ожидает классический игровой процесс, расширенный для нового поколения,'
                     'и графика под стать анимационному фильму 2016 года Ratchet & Clank™. ' ,
         publisher_id=4, poster="https://upload.wikimedia.org/wikipedia/en/3/37/Ratchet_and_Clank_cover.jpg"),
    Game(game_name="Infamous Second Son", genre="action-adventure", release_date=datetime.date(2014, 3, 21),
         price=20.00, description='Воспользуйтесь сверхспособностями Делсина Роу. Принимайте решения, от которых'
                                  'зависит судьба города и людей вокруг вас.' ,publisher_id=4,
         poster="https://upload.wikimedia.org/wikipedia/en/3/34/Infamous_second_son_boxart.jpg"),
    Game(game_name="The Legend of Zelda: Breath of the Wild", genre="action-adventure",
         release_date=datetime.date(2017, 3, 3), price=50.00,
         description='Не осталось ничего: ни королевства, ни воспоминаний. После столетнего сна Линк просыпается в мире,'
                     ' который он совсем не помнит. Чтобы вернуть воспоминания, легендарному герою предстоит исследовать'
                     ' огромный мир, таящий в себе немало опасностей. Но времени у него мало: Хайрул может исчезнуть с'
                     ' лица земли навсегда. Вооружившись тем, что смог найти, Линк отправляется на поиски ответов и того,'
                     ' что поможет ему выжить.' ,publisher_id=5,
         poster="https://upload.wikimedia.org/wikipedia/en/c/c6/The_Legend_of_Zelda_Breath_of_the_Wild.jpg"),
    Game(game_name="Super Mario Odyssey", genre="platform", release_date=datetime.date(2017, 10, 27), price=50.00,
         description='Марио отправится в кругосветное путешествие на летучем корабле под названием «Одиссея».'
                     'Перед тем как отчалить в новое царство, корабль нужно заправить, собрав несколько лун энергии.'
                     'Кто знает, куда он направится сегодня?' ,
         publisher_id=5, poster="https://upload.wikimedia.org/wikipedia/en/8/8d/Super_Mario_Odyssey.jpg"),
    Game(game_name="Super Smash Bros. Ultimate", genre="fighting", release_date=datetime.date(2018, 12, 7), price=60.00,
         description='Вышибайте соперников с арены в этой захватывающей экшен-игре. Более зрелищные битвы,'
                     'новые предметы, новые атаки, новые варианты защиты и другие нововведения не дадут вам оторваться'
                     'от экрана, где бы вы ни играли: дома или в пути.',publisher_id=5,
         poster="https://upload.wikimedia.org/wikipedia/en/5/50/Super_Smash_Bros._Ultimate.jpg"),
    Game(game_name="Splatoon 2", genre="third-person shooter", release_date=datetime.date(2017, 7, 21), price=50.00,
         description='Захватывай территорию, закрашивая ее краской своей команды в напряженных битвах 4 на 4. Побеждает'
                     'команда, закрасившая больше! Чтобы одержать верх, нужно действовать сообща и умело превращаться'
                     'из инклинга в кальмара, и наоборот. Вперед, в бой за район!',publisher_id=5,
         poster="https://upload.wikimedia.org/wikipedia/en/4/49/Splatoon_2.jpg"),
    Game(game_name="Animal Crossing: New Leaf", genre="social simulation", release_date=datetime.date(2012, 11, 8),
         price=15.00, description='Переселяясь в новый город, обзавестись друзьями непросто. Особенно непросто, если'
                                  'вы — мэр города. Приготовьтесь к новой жизни в городке, где вы можете сделать все'
                                  'как хотите в игре Animal Crossing: New Leaf, созданной для Nintendo 3DS и Nintendo'
                                  '3DS XL.' ,publisher_id=5,
         poster="https://upload.wikimedia.org/wikipedia/en/0/04/AnimalCrossingNewLeafNABoxart.jpg")
]

#db.session.bulk_save_objects(games)
#db.session.commit()

publishers = [
    Publisher(publisher_name="Ubisoft"),
    Publisher(publisher_name="EA"),
    Publisher(publisher_name="Activision"),
    Publisher(publisher_name="Sony"),
    Publisher(publisher_name="Nintendo")
]

#db.session.bulk_save_objects(publishers)
#db.session.commit()

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

#db.session.bulk_save_objects(platforms)
#db.session.commit()

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

