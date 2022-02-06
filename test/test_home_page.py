import re
from random import randrange

from model.contact import Contact


def test_name_on_home_page(app):
    old_contacts = app.contact.get_contact_list()
    index = randrange(len(old_contacts))
    contact_from_home_page = app.contact.get_contact_list()[index]
    contact_from_edit_page = app.contact.get_contact_info_from_edit_page(index)
    assert contact_from_home_page.firstname == contact_from_edit_page.firstname
    assert contact_from_home_page.lastname == contact_from_edit_page.lastname


def test_addres_on_home_page(app):
    old_contacts = app.contact.get_contact_list()
    index = randrange(len(old_contacts))
    contact_from_home_page = app.contact.get_contact_list()[index]
    contact_from_edit_page = app.contact.get_contact_info_from_edit_page(index)
    assert contact_from_home_page.address == contact_from_edit_page.address


def test_emails_on_home_page(app):
    old_contacts = app.contact.get_contact_list()
    index = randrange(len(old_contacts))
    contact_from_home_page = app.contact.get_contact_list()[index]
    contact_from_edit_page = app.contact.get_contact_info_from_edit_page(index)
    assert contact_from_home_page.all_emails_from_home_page == merge_emails_like_on_home_page(contact_from_edit_page)


def test_phones_on_home_page(app):
    old_contacts = app.contact.get_contact_list()
    index = randrange(len(old_contacts))
    contact_from_home_page = app.contact.get_contact_list()[index]
    contact_from_edit_page = app.contact.get_contact_info_from_edit_page(index)
    assert contact_from_home_page.all_phones_from_home_page == merge_phones_like_on_home_page(contact_from_edit_page)


def test_phones_on_contact_view_page(app):
    old_contacts = app.contact.get_contact_list()
    index = randrange(len(old_contacts))
    contact_from_view_page = app.contact.get_contact_from_view_page(index)
    contact_from_edit_page = app.contact.get_contact_info_from_edit_page(index)
    assert contact_from_view_page.home == contact_from_edit_page.home
    assert contact_from_view_page.mobile == contact_from_edit_page.mobile
    assert contact_from_view_page.work == contact_from_edit_page.work
    assert contact_from_view_page.phone2 == contact_from_edit_page.phone2


def clear(s):
    return re.sub("[() -]", "", s)


def merge_phones_like_on_home_page(contact):
    return "\n".join(filter(lambda x: x != "",
                            map(lambda x: clear(x), filter(lambda x: x is not None,
                                                           [contact.home,
                                                            contact.mobile, contact.work,
                                                            contact.phone2]))))


def merge_emails_like_on_home_page(contact):
    return "\n".join(filter(lambda x: x != "", filter(lambda x: x is not None, [contact.email,
                                                                                contact.email2, contact.email3])))


def test_all_contact_home_page_db(app, db, check_ui):
    db_contacts = db.get_contact_list()
    db_contacts = sorted(db_contacts, key=Contact.id_or_max)
    contacts_from_home_page = sorted(app.contact.get_contact_list(), key=Contact.id_or_max)
    assert len(db_contacts) == len(contacts_from_home_page)
    assert db_contacts == contacts_from_home_page
    for number in db_contacts:
        number.all_emails_from_home_page = merge_emails_like_on_home_page(number)
        number.all_phones_from_home_page = merge_phones_like_on_home_page(number)
    for i in range(len(db_contacts)):
        assert db_contacts[i].id == contacts_from_home_page[i].id
        assert db_contacts[i].firstname == contacts_from_home_page[i].firstname
        assert db_contacts[i].lastname == contacts_from_home_page[i].lastname
        assert db_contacts[i].address == contacts_from_home_page[i].address
        assert db_contacts[i].all_phones_from_home_page == contacts_from_home_page[i].all_phones_from_home_page
        assert db_contacts[i].all_emails_from_home_page == contacts_from_home_page[i].all_emails_from_home_page
        print(str(i))
        print(db_contacts[i])
        print(contacts_from_home_page[i])

