from datetime import datetime
from src import db


relationship_table = db.Table(
    "tag_to_notes",
    db.Model.metadata,
    db.Column("notes_id", db.ForeignKey("notes.id")),
    db.Column("tags_id", db.ForeignKey("tags.id")),
)


class ContactBook(db.Model):
    __tablename__ = 'contacts'
    id = db.Column('id', db.Integer, primary_key=True)
    name = db.Column('name', db.String(50), nullable=False)
    phone = db.Column('phone', db.String(12), nullable=True)
    birthday = db.Column('birthday', db.DateTime, nullable=True)
    email = db.Column('email', db.String(100), nullable=True)


class Note(db.Model):
    __tablename__ = "notes"
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(280), nullable=False)
    status = db.Column(db.Boolean, default=False)
    added = db.Column(db.DateTime, default=datetime.now())
    tags = db.relationship("Tag", secondary=relationship_table, back_populates="notes")


class Tag(db.Model):
    __tablename__ = "tags"
    id = db.Column(db.Integer, primary_key=True)
    tag = db.Column(db.String(15), nullable=False, unique=True)
    notes = db.relationship("Note", secondary=relationship_table, back_populates="tags")

    def __repr__(self) -> str:
        return self.tag
