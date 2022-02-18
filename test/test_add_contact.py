from model.contact import Contact
from model.group import Group
import random


def test_add_contact(app, db, json_contacts, check_ui):
    contact = json_contacts
    old_contacts = db.get_contact_list()
    app.contact.create(contact)
    new_contacts = db.get_contact_list()
    old_contacts.append(contact)
    assert sorted(old_contacts, key=Contact.id_or_max) == sorted(new_contacts, key=Contact.id_or_max)
    if check_ui:
        assert sorted(new_contacts, key=Contact.id_or_max) == sorted(app.contact.get_contact_list(),
                                                                     key=Contact.id_or_max)


def test_add_contact_in_group(app, orm, db):
    if len(db.get_contact_list()) == 0:
        app.contact.create(Contact(firstname="test"))
    if len(db.get_group_list()) == 0:
        app.group.create(Group(name="test"))
    contacts = db.get_contact_list()
    contact0 = random.choice(contacts)
    groups = db.get_group_list()
    group = random.choice(groups)
    if contact0.id not in group.name:
        app.contact.add_contact_in_group(contact0.id, group.name)
    else:
        app.contact.delete_contact_in_group(contact0.id, group.name)
        app.contact.add_contact_in_group(contact0.id, group.name)
    contacts_in_group = orm.get_contacts_in_group(group)
    assert Contact in contacts_in_group
