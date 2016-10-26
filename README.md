# AddressBook
## Install
```
python3 setup.py install
```
## Run tests
### Install test requirements
```
pip install -r requirements-test.txt
```
### Run
```
python3 -m pytest test
```
## API
### AddressBook
#### Construct addressbook object
```
from addressbook import AddressBook
bool = AddressBook()
```
You can optionally pass own Storage object to AddressBook constructor, to store objects in database. By default it uses `addressbook.memory_storage.AddressBookMemoryStore`
#### Construct person object
```
person = book.create_person(first_name, last_name, emails=[], phones=[], addresses=[])
```
where `first_name` and `last_name` are first and last name string.

`emails`, `phones`, `addresses` - are lists of strings

#### Construct group object
```
group = book.create_group(name)
```

`name` - a name for a group

#### Find person by name
```
book.person_by_name(first_name, last_name)
```
You need to provide either first name, last name, or both,
returns a list of matching persons

#### Find person by email
```
book.person_by_email(email)
```
You need to provide either email or email prefix,
returns a list of matching persons

### Person
#### Attributes
- first_name
- last_name
- emails
- phones
- addresses
- groups


#### Add person to group
```
person.add_to_group(group)
```

### Group
#### Attributes
- name
- members

#### Add person to group
```
group.add_member(person)
```

## Questions
#### Q: Find person by email address (can supply any substring, ie. "comp" should work assuming "alexander@company.com" is an email address in the address book) - discuss how you would implement this without coding the solution.
A: I can propose 3 solutions:

1. Construct regex like `.*comp.*` and loop trough the list of all email. Return matching
2. Create suffix tree instead of prefix tree (`addressbook.memory_storage.index`), which allows to search by any substring
3. Pass database-based storage to AddressBook constructor and use databases `LIKE` or similar

I would choose either 2 or 3. 2 requires more coding, but provides reasonable perfomance, while 3 delegates search to the database.
1 is good for small data and it also doesn't produce much memory overhead.
