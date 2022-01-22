from model.contact import Contact
import pytest
import random
import string


def random_string(prefix, maxlen):
    symbols = string.ascii_letters + string.digits
    return prefix + "".join([random.choice(symbols) for i in range(random.randrange(maxlen))])


testdata = [Contact(firstname="", middlename="", lastname="",
                    nickname="", title="",
                    company="", address="",
                    home="", mobile="", work="", phone2="",
                    email="", email2="", email3="")] + [
               Contact(firstname=random_string("firstname", 15), middlename=random_string("middlename", 20),
                       lastname=random_string("lastname", 15),
                       nickname=random_string("nick", 25), title=random_string("title", 15),
                       company=random_string("company", 15), address=random_string("address", 20),
                       home=random_string("phone", 15), mobile=random_string("mobile", 15),
                       work=random_string("work", 15), phone2=random_string("phone2", 15),
                       email=random_string("email", 20), email2=random_string("email2", 25),
                       email3=random_string("email3", 15))
               for i in range(1)

           ]


@pytest.mark.parametrize("contact", testdata, ids=[repr(x) for x in testdata])
def test_add_contact(app, contact):
    old_contacts = app.contact.get_contact_list()
    app.contact.create(contact)
    assert len(old_contacts) + 1 == app.contact.count()
    new_contacts = app.contact.get_contact_list()
    old_contacts.append(contact)
    assert sorted(old_contacts, key=Contact.id_or_max) == sorted(new_contacts, key=Contact.id_or_max)
