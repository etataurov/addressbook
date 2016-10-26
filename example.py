import addressbook

book = addressbook.AddressBook()
emails = ["tatauroff@gmail.com", "etataurov@me.com"]
phones = ["89221116386"]
addresses = ["Lenina st"]
person = book.create_person(
    first_name="Eugene", last_name="Tataurov",
    emails=emails, phones=phones, addresses=addresses
)
group = book.create_group("Friends")
person.add_to_group(group)
print(person)
