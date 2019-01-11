import sys
from secrets import token

import blockscore

# these are countries without postal codes
countries_without_ps = ["AO", "BS", "CI", "ER", "GY", "HK", "IE", "KE", "MO", "AN", "PA", "QA", "KN", "ZA", "TT", "ZW"]


class People():

    def __init__(self):

        self.client = blockscore.Client(token)

    # this part creates a person and prints "invalid person" or "valid person" according to the status
    def create_person(self):

        address_postal_code = None
        birth_ISO = input("birth date in ISO format*: ")
        document_type = input("Document type*: ")
        document_value = input("Document value*: ")
        first_name = input("First name*: ")
        middle_name = input("middle name: ")
        last_name = input("Last name*: ")
        address_street1 = input("address street1*: ")
        address_street2 = input("address street2: ")
        address_city = input("address city*: ")
        address_subdivision = input("address subdivision*: ")
        address_country_code = input("country code*: ")

        # address_postal_code is currently None but if the country has postal codes it will ask a postal code and
        # overwrite it to our variable
        if address_country_code not in countries_without_ps:
            address_postal_code = input("postal code*: ")

        note = input("note: ")

        birth_year, birth_month, birth_day = birth_ISO.split("-")

        person = self.client.people.create({
            "name_first": first_name,
            "name_middle": middle_name,
            "name_last": last_name,
            "birth_day": birth_day,
            "birth_month": birth_month,
            "birth_year": birth_year,
            "document_type": document_type,
            "document_value": document_value,
            "address_street1": address_street1,
            "address_street2": address_street2,
            "address_city": address_city,
            "address_subdivision": address_subdivision,
            "address_postal_code": address_postal_code,
            "address_country_code": address_country_code,
            "note": note
         })

        person = person.body
        print(person["status"], "person")

    def retrieve_person(self, ID):

        person = self.client.people.retrieve(ID)
        person = person.body
        print(person)

    def list_people(self):

        people = self.client.people.all()
        people = people.body
        print(people)


def main():

    # creating an object
    user = People()

    while True:
        action = input("Type 'create' to create a person, 'retrieve' to retrieve a person,'list' to list the people or"
                       " 'quit' to close the application: ")

        try:
            if action == "create":
                user.create_person()

            elif action == "retrieve":
                ID = input("id: ")
                user.retrieve_person(ID)

            elif action == "list":
                user.list_people()

            elif action == "quit":
                sys.exit(0)

            else:
                print("invalid action")
                sys.exit(1)

        # catching the invalid inputs
        except blockscore.error.ValidationError:
            print("invalid inputs")
            sys.exit(1)


if __name__ == "__main__":
    main()
