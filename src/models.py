from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# <------------------- CHARACTER -------------------------------------------------------->

class Character(db.Model):
    __tablename__ = 'character'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False, unique=True)
    species = db.Column(db.String(250), nullable=False)
    gender = db.Column(db.String(250), nullable=False)
    is_alive = db.Column(db.Boolean, default=True, nullable=False)

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "species": self.species,
            "gender": self.gender,
            "is_alive": self.is_alive
        }

charactersFavs = db.Table("charactersFav",
     db.Column("user_id", db.Integer, db.ForeignKey("user.id"), primary_key=True),
     db.Column("character_id", db.Integer, db.ForeignKey("character.id"), primary_key=True)
)


# <------------------- LOCATION -------------------------------------------------------->

class Location(db.Model):
    __tablename__ = 'location'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False, unique=True)
    type = db.Column(db.String(250), nullable=False)
    dimension = db.Column(db.String(250), nullable=False)

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "type": self.type,
            "dimension": self.dimension
        }

locationsFavs = db.Table("locationsFav",
     db.Column("user_id", db.Integer, db.ForeignKey("user.id"), primary_key=True),
     db.Column("location_id", db.Integer, db.ForeignKey("location.id"), primary_key=True)
)


# <------------------- EPISODE -------------------------------------------------------->

class Episode(db.Model):
    __tablename__ = 'episode'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False, unique=True)
    air_date = db.Column(db.String(250), nullable=False)
    episode = db.Column(db.String(250), nullable=False)

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "air_date": self.air_date,
            "episode": self.episode
        }

episodesFavs = db.Table("episodesFav",
     db.Column("user_id", db.Integer, db.ForeignKey("user.id"), primary_key=True),
     db.Column("episode_id", db.Integer, db.ForeignKey("episode.id"), primary_key=True)
)


# <------------------- USER -------------------------------------------------------->

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(20), nullable=False, unique=True)
    first_name = db.Column(db.String(25), nullable=False)
    last_name = db.Column(db.String(25), nullable=False)
    email = db.Column(db.String(25), nullable=False, unique=True)
    password = db.Column(db.String(25), nullable=False, unique=True)
    is_active = db.Column(db.Boolean, default=True)
    charactersFav = db.relationship(Character,
                    secondary=charactersFavs,
                    lazy='subquery',
                    backref=db.backref('users', lazy=True))
    locationsFav = db.relationship(Location,
                    secondary=locationsFavs,
                    lazy='subquery',
                    backref=db.backref('users', lazy=True))
    episodesFav = db.relationship(Episode,
                    secondary=episodesFavs,
                    lazy='subquery',
                    backref=db.backref('users', lazy=True))


    def serialize(self):
        return {
            "id": self.id,
            "user_name": self.user_name,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            "is_active": self.is_active,
            "charactersFav": self.obtain_charactersFav(),
            "locationsFav": self.obtain_locationsFav(),
            "episodesFav": self.obtain_episodesFav()
            # do not serialize the password, its a security breach  
        }

    def obtain_charactersFav(self):
        return list(map(lambda x: x.serialize(), self.charactersFav))

    def obtain_locationsFav(self):
        return list(map(lambda x: x.serialize(), self.locationsFav))

    def obtain_episodesFav(self):
        return list(map(lambda x: x.serialize(), self.episodesFav))
