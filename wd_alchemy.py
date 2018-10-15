
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, BigInteger, Text, String, ForeignKey
from sqlalchemy.orm import relationship

Base = declarative_base()


class CRace(Base):
    __tablename__ = "races"

    race_id = Column(Integer, primary_key=True)
    mask = Column(Integer)
    side = Column(String(20))
    name = Column(String(50))

    def __init__(self, id, mask, side, name):
        self.race_id = id
        self.mask = mask
        self.side = side
        self.name = name

    def __repr__(self):
        return "Race '%s'" % (self.name)


class CClass(Base):
    __tablename__ = "classes"
    class_id = Column(Integer, primary_key=True)
    mask = Column(Integer)
    powerType = Column(String(20))
    name = Column(String(50))

    def __init__(self, id, mask, powerType, name):
        self.class_id = id
        self.mask = mask
        self.powerType = powerType
        self.name = name

    def __repr__(self):
        return "Class '%s'" % (self.name)


class CItemLoot(Base):
    __tablename__ = 'item_loot'
    id = Column(Integer, primary_key=True)
    type = Column(String(50))
    character_name = Column(String(50), ForeignKey('guild_members.name'))
    timestamp = Column(BigInteger)
    itemId = Column(Integer, ForeignKey('items2.id'))
    context = Column(String(50))
    posted = Column(Integer)

    member_obj = relationship("CMember")
    item_obj = relationship("CItem")

    def __init__(self, type, character, timestamp, itemId, context, **other):
        self.type = type
        self.character_name = character
        self.timestamp = timestamp
        self.itemId = itemId
        self.posted = 0
        self.context = context

    def __repr__(self):
        return "Class '%s' '%s" % (self.character_name, self.itemId)


class CMember(Base):
    __tablename__ = 'guild_members'

    member_id = Column(Integer, primary_key=True)
    name = Column(String(100))
    realm = Column(String(50))
    class_id = Column(Integer, ForeignKey('classes.class_id'))
    race = Column(Integer, ForeignKey('races.race_id'))
    gender = Column(Integer)
    level = Column(Integer)
    achievementPoints = Column(Integer)
    thumbnail = Column(String(100))
    rank = Column(Integer)
    posted = Column(Integer)
    isMember = Column(Integer)
    is_check = Column(Integer)

    class_obj = relationship("CClass")
    race_obj = relationship("CRace")

    # class_obj = relationship("CClass",foreign_keys='CClass.class_id')
    # race_obj = relationship("CRace",foreign_keys='CRace.race_id')

    def __init__(self, name, realm, class_id, race, gender, level, achievementPoints, thumbnail, **others):
        self.name = name
        self.realm = realm
        self.class_id = class_id
        self.race = race
        self.gender = gender
        self.level = level
        self.achievementPoints = achievementPoints
        self.thumbnail = thumbnail
        self.rank = 0
        self.posted = 0
        self.isMember = 1
        self.is_check = 0

    def __repr__(self):
        return "Class '%s'" % (self.name)


class CItem(Base):
    __tablename__ = 'items2'

    id = Column(Integer, primary_key=True)
    description = Column(String(200))
    name = Column(String(100))
    icon = Column(String(100))
    itemLevel = Column(Integer)

    def __init__(self, id, description, name, icon, itemLevel, **other):
        self.id = id
        self.description = description
        self.name = name
        self.icon = icon
        self.itemLevel = itemLevel

    def __repr__(self):
        return "Race '%s'" % (self.name)


class CGuildAchievement(Base):
    __tablename__ = 'guild_achievement'
    id = Column(Integer, primary_key=True)
    character_name = Column(String(100), ForeignKey('guild_members.name'))
    timestamp = Column(BigInteger)
    context = Column(String(50))
    achievement_id = Column(Integer)
    title = Column(String(100))
    description = Column(String(200))
    icon = Column(String(100))
    posted = Column(Integer)

    member_obj = relationship("CMember")

    def __init__(self, character, timestamp, context, achievement, **other):
        self.character_name = character
        self.timestamp = timestamp
        self.context = context
        self.achievement_id = achievement['id']
        self.title = achievement['title']
        self.description = achievement['description']
        self.icon = achievement['icon']
        self.posted = 0

    def __repr__(self):
        return "Guild Achievement '%s'" % (self.id)


class CMemberAchievement(Base):
    __tablename__ = 'player_achievement'
    id = Column(Integer, primary_key=True)
    character_name = Column(String(100), ForeignKey('guild_members.name'))
    timestamp = Column(BigInteger)
    context = Column(String(50))
    achievement_id = Column(Integer)
    title = Column(String(100))
    description = Column(String(200))
    icon = Column(String(100))
    posted = Column(Integer)

    member_obj = relationship("CMember")

    def __init__(self, character, timestamp, context, achievement, **other):
        self.character_name = character
        self.timestamp = timestamp
        self.context = context
        self.achievement_id = achievement['id']
        self.title = achievement['title']
        self.description = achievement['description']
        self.icon = achievement['icon']
        self.posted = 0

    def __repr__(self):
        return "Player Achievement '%s'" % (self.id)
