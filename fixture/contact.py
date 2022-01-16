from model.contact import Contact


class ContactHelper:
    def __init__(self, app):
        self.app = app

    def open_contact_page(self):
        wd = self.app.wd
        wd.get("http://localhost/addressbook/addressbook/")

    def create(self, contact):
        wd = self.app.wd
        self.open_contact_page()
        # init contacts creation
        wd.find_element_by_link_text("add new").click()
        # fill contacts form
        self.fill_contact_form(contact)
        # submit contacts creation
        wd.find_element_by_name("submit").click()
        self.return_to_home_page()
        self.contact_cache = None

    def fill_contact_form(self, contact):
        wd = self.app.wd
        self.change_value("firstname", contact.firstname)
        self.change_value("middlename", contact.middlename)
        self.change_value("lastname", contact.lastname)
        self.change_value("nickname", contact.nickname)
        self.change_value("title", contact.title)
        self.change_value("company", contact.company)
        self.change_value("address", contact.address)
        self.change_value("home", contact.home)
        self.change_value("mobile", contact.mobile)

    def change_value(self, field_name, text):
        wd = self.app.wd
        if text is not None:
            wd.find_element_by_name(field_name).click()
            wd.find_element_by_name(field_name).clear()
            wd.find_element_by_name(field_name).send_keys(text)

    def delete_first_contact(self):
        self.delete_contact_by_index(0)

    def select_first_contact(self):
        wd = self.app.wd
        wd.find_element_by_name("selected[]").click()

    def select_contact_by_index(self, index):
        wd = self.app.wd
        wd.find_elements_by_name("selected[]")[index].click()

    def delete_contact_by_index(self, index):
        wd = self.app.wd
        self.open_contact_page()
        self.select_contact_by_index(index)
        # submit deletion
        wd.find_element_by_xpath("//input[@value='Delete']").click()
        wd.switch_to.alert.accept()
        self.contact_cache = None

    def modify_first_contact(self):
        self.modify_contact_by_index(0)

    def modify_contact_by_index(self, index, new_contacts_data):
        wd = self.app.wd
        self.open_contact_page()
        self.select_contact_by_index(index)
        # open modification form
        wd.find_element_by_xpath("//img[@alt='Edit']").click()
        # fill contacts form
        self.fill_contact_form(new_contacts_data)
        # submit modification
        wd.find_element_by_name("update").click()
        self.return_to_home_page()
        self.contact_cache = None

    def return_to_home_page(self):
        wd = self.app.wd
        wd.find_element_by_link_text("home page").click()

    def count(self):
        wd = self.app.wd
        self.open_contact_page()
        return len(wd.find_elements_by_name("selected[]"))

    contact_cache = None

    def get_contact_list(self):
        if self.contact_cache is None:
            wd = self.app.wd
            self.open_contact_page()
            self.contact_cache = []
            for element in wd.find_elements_by_name("entry"):
                cells = element.find_elements_by_css_selector("td.center")
                firstname = cells.text
                lastname = cells.text
                id = cells.find_element_by_name("selected[]").get_attribute("value")
                self.contact_cache.append(Contact(firstname=firstname, lastname=lastname, id=id))
        return list(self.contact_cache)
