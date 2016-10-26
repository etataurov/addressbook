from unittest import TestCase
from addressbook import AddressBook
import pytest


class TestAddressBookBasic(TestCase):
    def setUp(self):
        self.book = AddressBook()

    def test_create_address_book(self):
        assert len(self.book.persons) == 0
        assert len(self.book.groups) == 0

    def test_add_person(self):
        person = self.book.create_person(first_name="Test", last_name="Man")
        assert len(self.book.persons) == 1
        assert person.first_name == "Test"
        assert person.last_name == "Man"

    def test_add_person_with_attributes(self):
        emails = ["1@test.com", "2@test.com"]
        phones = ["123", "456"]
        addresses = ["Baker st", "Lenin st"]
        person = self.book.create_person(
            first_name="Test", last_name="Man",
            emails=emails, phones=phones, addresses=addresses
        )
        assert person.emails == emails
        assert person.phones == phones
        assert person.addresses == addresses

    def test_person_wrong_attribute_types(self):
        phones = [12345]
        with pytest.raises(AssertionError):
            self.book.create_person(
                first_name="Test", last_name="Man",
                phones=phones
            )

    def test_add_group(self):
        group = self.book.create_group(name="Friends")
        assert len(self.book.groups) == 1
        assert group.name == "Friends"

    def test_group_members(self):
        group = self.book.create_group(name="Friends")
        person1 = self.book.create_person(first_name="Test", last_name="Man")
        person2 = self.book.create_person(first_name="Test", last_name="Dog")
        group.add_member(person1)
        group.add_member(person2)
        assert len(group.members) == 2
        assert sorted(group.members, key=lambda p: p.last_name) == [person2, person1]

    def test_person_groups(self):
        group1 = self.book.create_group(name="Friends")
        group2 = self.book.create_group(name="Foes")
        person = self.book.create_person(first_name="Test", last_name="Man")
        group1.add_member(person)
        group2.add_member(person)
        assert len(person.groups) == 2
        assert sorted(person.groups, key=lambda p: p.name) == [group2, group1]


class TestAddressBookSearchByName(TestCase):
    def setUp(self):
        self.book = AddressBook()
        self.book.create_person(first_name="Test", last_name="Dog")
        self.book.create_person(first_name="Mike", last_name="Dog")

    def test_find_person_by_first_name(self):
        person = self.book.create_person(first_name="Test", last_name="Man")
        result = self.book.person_by_name(first_name="Test")
        assert len(result) == 2
        assert person in result

    def test_find_person_by_last_name(self):
        person = self.book.create_person(first_name="Test", last_name="Man")
        result = self.book.person_by_name(last_name="Man")
        assert len(result) == 1
        assert person in result

    def test_find_person_by_both(self):
        person = self.book.create_person(first_name="Test", last_name="Man")
        result = self.book.person_by_name(first_name="Test", last_name="Man")
        assert len(result) == 1
        assert person in result

    def test_find_person_no_result(self):
        self.book.create_person(first_name="Test", last_name="Man")
        result = self.book.person_by_name(first_name="George", last_name="Man")
        assert len(result) == 0

    def test_find_person_wrong_parameters(self):
        with pytest.raises(AssertionError):
            self.book.person_by_name(first_name=None, last_name=None)


class TestAddressBookSearchByEmail(TestCase):
    def setUp(self):
        self.book = AddressBook()

    def test_find_person_by_email(self):
        person = self.book.create_person(first_name="Test", last_name="Man", emails=["test@example.com"])
        result = self.book.person_by_email("test@example.com")
        assert len(result) == 1
        assert result[0] == person

    def test_find_person_by_email_prefix(self):
        person = self.book.create_person(first_name="Test", last_name="Man", emails=["test@example.com"])
        result = self.book.person_by_email("test")
        assert len(result) == 1
        assert result[0] == person

    def test_find_person_by_email_no_result(self):
        person = self.book.create_person(first_name="Test", last_name="Man", emails=["test@example.com"])
        result = self.book.person_by_email("foo")
        assert len(result) == 0
