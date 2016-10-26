import enum
import weakref

from collections import defaultdict


class AttributeType(enum.Enum):
    email = "email"
    phone = "phone"
    street = "street"


class PersonAttribute:
    def __init__(self, person, value):
        self._person = weakref.ref(person)
        self.value = value

    @property
    def person(self):
        return self._person()

    def __repr__(self):
        return "PersonAttribute(person={!r}, value='{!r}')".format(self._person(), self.value)

    def __str__(self):
        return str(self.value)


class Person:
    def __init__(self, first_name, last_name):
        self.first_name = first_name
        self.last_name = last_name
        self._attributes = defaultdict(list)
        self._store = None

    def __repr__(self):
        return "Person(first_name='{}', last_name='{}')".format(self.first_name, self.last_name)

    def __str__(self):
        parts = ["{} {}".format(self.first_name, self.last_name)]
        if self.groups:
            parts.append("Groups: {}".format(", ".join(g.name for g in self.groups)))
        if self.emails:
            parts.append("Email addresses: {}".format(", ".join(v for v in self.emails)))
        if self.phones:
            parts.append("Phone addresses: {}".format(", ".join(v for v in self.phones)))
        if self.addresses:
            parts.append("Street addresses: {}".format(", ".join(v for v in self.addresses)))
        return "\n".join(parts)

    @property
    def store(self):
        return self._store()

    @store.setter
    def store(self, value):
        self._store = weakref.ref(value)

    @property
    def groups(self):
        return self.store.get_person_groups(self)

    @property
    def emails(self):
        return self._get_attributes_values(AttributeType.email)

    @property
    def phones(self):
        return self._get_attributes_values(AttributeType.phone)

    @property
    def addresses(self):
        return self._get_attributes_values(AttributeType.street)

    def _get_attributes_values(self, attr_type):
        return [a.value for a in self._attributes[attr_type]]

    def _add_attribute(self, attr_type, attr_value):
        attr = PersonAttribute(self, attr_value)
        self.store.register_attribute(attr_type, attr)
        self._attributes[attr_type].append(attr)

    def add_email_address(self, value):
        self._add_attribute(AttributeType.email, value)

    def add_phone_number(self, value):
        self._add_attribute(AttributeType.phone, value)

    def add_street_address(self, value):
        self._add_attribute(AttributeType.street, value)

    def add_to_group(self, group):
        group.add_member(self)


class Group:
    def __init__(self, name):
        self.name = name
        self._members = weakref.WeakSet()

    def __repr__(self):
        return "Group(name='{}')".format(self.name)

    def __str__(self):
        return self.name

    @property
    def members(self):
        return list(self._members)

    def add_member(self, person):
        self._members.add(person)
