from collections import defaultdict
from .models import Person, Group, AttributeType
from .index import AttributeIndex


class AddressBookMemoryStore:
    def __init__(self):
        self._persons = []
        self._groups = []
        self.indexed = {AttributeType.email}
        self.indexes = defaultdict(AttributeIndex)

    @property
    def persons(self):
        return self._persons

    @property
    def groups(self):
        return self._groups

    def create_person(self, *args, **kwargs):
        emails = kwargs.pop('emails', None) or []
        phones = kwargs.pop('phones', None) or []
        addresses = kwargs.pop('addresses', None) or []
        person = Person(*args, **kwargs)
        person.store = self
        for email in emails:
            person.add_email_address(email)
        for phone in phones:
            person.add_phone_number(phone)
        for address in addresses:
            person.add_street_address(address)
        self._persons.append(person)
        return person

    def create_group(self, *args, **kwargs):
        group = Group(*args, **kwargs)
        self._groups.append(group)
        return group

    def get_person_groups(self, person):
        return [
            group for group in self._groups
            if person in group._members
        ]

    def register_attribute(self, attr_type, attr):
        if attr_type in self.indexed:
            self.indexes[attr_type].add(attr)

    def person_by_name(self, first_name=None, last_name=None):
        return [
            person for person in self._persons
            if (first_name is None or person.first_name == first_name) and (last_name is None or person.last_name == last_name)
        ]

    def person_by_email(self, email):
        return [a.person for a in self.indexes[AttributeType.email].search(email)]
