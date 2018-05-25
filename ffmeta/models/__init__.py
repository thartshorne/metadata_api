from sqlalchemy import Column, Integer, Text, String, ForeignKey
from sqlalchemy.orm import relationship

from ffmeta.models.db import Base


class Variable(Base):
    __tablename__ = "variable"

    # Define table fields
    id = Column(Integer, primary_key=True)
    name = Column(Text)
    label = Column(Text)
    old_name = Column(Text)
    data_type = Column(Text)
    warning = Column(Integer)
    group_id = Column(Text)
    group_subid = Column(Text)
    data_source = Column(Text)
    respondent = Column(Text)
    wave = Column(Text)
    scope = Column(Text)
    section = Column(Text)
    leaf = Column(Text)

    responses = relationship('Response', backref='variable')
    topics = relationship('Topic', backref='variable')

    def __init__(self, name, label, old_name, data_type, warning, group_id, group_subid, data_source, respondent, wave, scope, section, leaf):
        self.name = name
        self.label = label
        self.old_name = old_name
        self.data_type = data_type
        self.warning = warning
        self.group_id = group_id
        self.group_subid = group_subid
        self.data_source = data_source
        self.respondent = respondent
        self.wave = wave
        self.scope = scope
        self.section = section
        self.leaf = leaf

    def __repr__(self):
        return "<Variable %r>" % self.name

    @property
    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "label": self.label,
            "old_name": self.old_name,
            "data_type": self.data_type,
            "warning": self.warning,
            "group_id": self.group_id,
            "group_subid": self.group_subid,
            "data_source": self.data_source,
            "respondent": self.respondent,
            "wave": self.wave,
            "scope": self.scope,
            "section": self.section,
            "leaf": self.leaf
        }


class Topic(Base):
    __tablename__ = "topic"

    id = Column(Integer, primary_key=True)
    name = Column(Text, ForeignKey("variable.name"))
    topic = Column(Text)

    umbrella = relationship('Umbrella', backref='topic_obj', uselist=False)

    def __init__(self, name, topic):
        self.name = name
        self.topic = topic

    def __repr__(self):
        return "<Topic %r>" % self.topic

    def __str__(self):
        return self.topic


class Umbrella(Base):
    __tablename__ = "umbrella"

    id = Column(Integer, primary_key=True)
    topic = Column(Text, ForeignKey("topic.topic"))
    umbrella = Column(Text)

    def __init__(self, topic, umbrella):
        self.topic = topic
        self.umbrella = umbrella

    def __repr__(self):
        return "<Umbrella %r>" % self.umbrella

    def __str__(self):
        return self.umbrella


class Response(Base):
    __tablename__ = "response"

    id = Column(Integer, primary_key=True)
    name = Column(Text, ForeignKey("variable.name"))
    label = Column(Text)
    value = Column(Integer)

    def __init__(self, name, label, value):
        self.name = name
        self.label = label
        self.value = value

    def __repr__(self):
        return "<Response %r>" % self.label


class Group(Base):
    __tablename__ = "group"

    id = Column(Integer, primary_key=True)
    group_id = Column(Text)
    count = Column(Integer)

    def __init__(self, group_id, count):
        self.group_id = group_id
        self.count = count

    def __repr__(self):
        return "<Group %r>" % self.group_id
