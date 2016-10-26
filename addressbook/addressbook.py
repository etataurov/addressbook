from .memory_storage import AddressBookMemoryStore


class AddressBook:
    def __init__(self, store=None):
        if store is None:
            self.store = AddressBookMemoryStore()
        else:
            self.store = store

    @property
    def persons(self):
        return self.store.persons

    @property
    def groups(self):
        return self.store.groups

    def create_person(self, first_name, last_name, emails=None, phones=None, addresses=None):
        return self.store.create_person(first_name, last_name, emails=emails, phones=phones, addresses=addresses)

    def create_group(self, name):
        return self.store.create_group(name)

    def person_by_name(self, first_name=None, last_name=None):
        assert not (
            first_name is None and last_name is None
        ), "You should provide either first_name or last_name or both"
        return self.store.person_by_name(first_name, last_name)

    def person_by_email(self, email):
        return self.store.person_by_email(email)
