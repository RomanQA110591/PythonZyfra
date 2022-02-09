from model.contact import Contact
from model.group import Group
import random


def test_delete_some_contact(app, db, check_ui):
    if len(db.get_contact_list()) == 0:
        app.contact.create(Contact(firstname="Test"))
    old_contacts = db.get_contact_list()
    contact = random.choice(old_contacts)
    app.contact.delete_contact_by_id(contact.id)
    new_contacts = db.get_contact_list()
    assert len(old_contacts) - 1 == len(new_contacts)
    old_contacts.remove(contact)
    assert old_contacts == new_contacts
    if check_ui:
        assert sorted(new_contacts, key=Contact.id_or_max) == sorted(app.contact.get_contact_list(),
                                                                     key=Contact.id_or_max)


def test_delete_some_contact_in_groups(app, orm, json_contacts, db):
    contact = json_contacts
    if len(db.get_contact_list()) == 0:
        app.contact.create(contact)
    if len(db.get_group_list()) == 0:
        app.group.create(Group(name="test"))
    contacts = db.get_contact_list()
    contact0 = random.choice(contacts)
    groups = db.get_group_list()
    group = random.choice(groups)
    if contact0.id in group.name:
        app.delete_contact_in_group(contact0.id, group.name)
    else:
        app.contact.add_contact_in_group(contact0.id, group.name)
        app.contact.delete_contact_in_group(contact0.id, group.name)
    new_contacts_in_group = orm.get_contacts_in_group(group)
    assert contact not in new_contacts_in_group
