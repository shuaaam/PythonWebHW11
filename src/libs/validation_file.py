def check_value(ab, phone, birthday, email):
    if not birthday and not email:
        ab.phone = phone
    elif birthday is not None and not email:
        ab.phone = phone
        ab.birthday = birthday
    elif birthday is not None and email != '':
        ab.phone = phone
        ab.birthday = birthday
        ab.email = email
    else:
        ab.phone = phone
        ab.birthday = birthday
        ab.email = email