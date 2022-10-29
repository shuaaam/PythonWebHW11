from datetime import datetime

from flask import render_template, request, redirect, url_for, flash
from src.models import Note, ContactBook, Tag
from src import db
from . import app
from src.libs.validation_file import check_value
from src.libs.validation_schemas import Birthday, Phone, Name, Email, DateIsNotValid


@app.route('/')
@app.route('/main')
def main_page():
    return render_template('Pages/main.html')


@app.route('/contactbook', strict_slashes=False, methods=['GET', 'POST'])
def contactbook():
    phone = ''
    birthday = None
    email = ''
    if request.method == 'POST':
        name = Name(request.form.get('name')).value
        try:
            phone = Phone(request.form.get('phone')).value
            birthday = Birthday(request.form.get('birthday')).value
            email = Email(request.form.get('email')).value
        except ValueError:
            flash('Invalid value')
            return redirect(url_for('contactbook'))
        except DateIsNotValid:
            flash('Invalid format, should be: y-m-d')
            return redirect(url_for('contactbook'))
        except AttributeError:
            flash('Invalid format')
            return redirect(url_for('contactbook'))
        cb = ContactBook(name=name, phone=phone, birthday=birthday, email=email)
        db.session.add(cb)
        db.session.commit()
        return redirect('/show_cb')
    else:
        return render_template('Pages/contactbook.html', back='/show_cb')


@app.route('/note', strict_slashes=False, methods=['GET', 'POST'])
def note():
    if request.method == 'POST':
        description = request.form.get('description')
        tags = request.form.getlist("tags")
        all_tags = []
        for tag in tags:
            all_tags.append(db.session.query(Tag).filter(Tag.tag == tag).first())
        note = Note(description=description, tags=all_tags)
        db.session.add(note)
        db.session.commit()
        return redirect('/show_note')
    else:
        tags = db.session.query(Tag).all()
    return render_template('Pages/note.html', back='/show_note', tags=tags)


@app.route('/tag', methods=['GET', 'POST'])
def tag():
    if request.method == 'POST':
        tags = request.form.get('tags')
        tag_ = Tag(tag=tags)
        db.session.add(tag_)
        db.session.commit()
        return redirect(url_for('note'))
    return render_template('Pages/tag.html', back='/show_note')


@app.route('/show_cb')
def show_ab():
    contactbook = db.session.query(ContactBook).all()
    return render_template('Pages/show_cb.html', back='/', contactbook=contactbook)


@app.route('/show_note')
def show_note():
    notes = db.session.query(Note).all()
    return render_template('Pages/show_note.html', back='/main', notes=notes)


@app.route('/status/<id>')
def done(id):
    note = db.session.query(Note).filter(Note.id == id).one()
    note.status = True
    db.session.commit()
    return redirect('/show_note')


@app.route('/change_ab/', methods=['POST', 'GET'])
def change_cb():
    phone = ''
    birthday = None
    email = ''
    if request.method == 'POST':
        id = request.form.get('id')
        try:
            phone = Phone(request.form.get('phone')).value
            birthday = Birthday(request.form.get('birthday')).value
            email = Email(request.form.get('email')).value
        except ValueError:
            print('Incorrect phone format')
        except DateIsNotValid:
            print('Incorrect birthday format')
        except AttributeError:
            print('Incorrect email format')
        cb = db.session.query(ContactBook).filter(ContactBook.id == int(id)).one()
        check_value(cb, phone, birthday, email)
        db.session.commit()
        return redirect('/show_cb')
    return render_template('Pages/change_cb.html', back='/show_cb')


@app.route('/delete_cb/', methods=['POST', 'GET'])
def delete_ab():
    if request.method == 'POST':
        id_ = request.form.get('id')
        db.session.query(ContactBook).filter(ContactBook.id == int(id_)).delete()
        db.session.commit()
        return redirect('/show_cb')

    return render_template('Pages/delete_cb.html', back='/show_cb')


@app.route('/change_note/', methods=['POST', 'GET'])
def change_note():
    if request.method == 'POST':
        id = request.form.get('id')
        description = request.form.get('description')
        tags = request.form.getlist("tags")
        all_tags = []
        for tag in tags:
            all_tags.append(db.session.query(Tag).filter(Tag.tag == tag).first())
        note = db.session.query(Note).filter(Note.id == int(id)).one()
        if note.status is True:
            pass
        else:
            note.tags = all_tags
            note.description = description
            db.session.commit()
            return redirect('/show_note')
    else:
        tags = db.session.query(Tag).all()
    return render_template('Pages/change_note.html', back='/show_note', tags=tags)


@app.route('/delete_note/', methods=['POST', 'GET'])
def delete_note():
    if request.method == 'POST':
        id_ = request.form.get('id')
        db.session.query(Note).filter(Note.id == int(id_)).delete()
        db.session.commit()
        return redirect('/show_note')

    return render_template('Pages/delete_note.html', back='/show_note')


@app.route('/delete_tag/', methods=['POST', 'GET'])
def delete_tag():
    if request.method == 'POST':
        tag = request.form.getlist('tags')
        for i in tag:
            db.session.query(Tag).filter(Tag.tag == i).delete()
        db.session.commit()
        return redirect('/show_note')
    else:
        tags = db.session.query(Tag).all()
    return render_template('Pages/delete_tag.html', back='/show_note', tags=tags)
