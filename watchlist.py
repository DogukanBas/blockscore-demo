import sys
from secrets import token

import blockscore

# these are the countries without postal codes

countries_without_ps = ["AO", "BS", "CI", "ER", "GY", "HK", "IE", "KE", "MO", "AN", "PA", "QA", "KN", "ZA", "TT", "ZW"]


class Candidate():
    def __init__(self):

        self.client = blockscore.Client(token)

    # creating a candidate
    def create_candidate(self, *args):

        # assigning object's variables
        identity = {
            'date_of_birth': birth_ISO,
            'identification': {
                "ssn": ssn,
                "passport": passport

            },
            'name': {
                'first': first_name,
                'middle': middle_name,
                'last': last_name
            },
            'address': {
                'street1': address_street1,
                'street2': address_street2,
                'city': address_city,
                'state': address_subdivision,
                'postal_code': address_postal_code,
                'country_code': address_country_code
            },
            'note': note

        }

        candidate = self.client.watchlists.create(**identity)

        print(candidate.body)

    # listing candidates
    def list_candidates(self):

        listed = self.client.watchlists.list()
        print(listed.body)

    # deleting a candidate
    def delete_candidate(self, ID):

        self.client.watchlists.delete(ID)
        print("The candidate has been deleted successfully")

    # editing a candidate
    def edit_candidate(self, ID, *args):

        keys = ["note", "date_of_birth", "ssn", "passport", "first", "middle", "last", "street1", "street2", "city",
                "state", "postal_code", "country_code"]

        zipped = dict(zip(keys, args))

        identity = {
            'date_of_birth': zipped["date_of_birth"],
            'identification': {
                "ssn": zipped["ssn"],
                "passport": zipped["passport"]

            },
            'name': {
                'first': zipped["first"],
                'middle': zipped["middle"],
                'last': zipped["last"]
            },
            'address': {
                'street1': zipped["street1"],
                'street2': zipped["street2"],
                'city': zipped["city"],
                'state': zipped["state"],
                'postal_code': zipped["postal_code"],
                'country_code': zipped["country_code"]
            },

            "note": zipped["note"]

        }

        edited_dict = {}
        for key,value in identity.items():
            if isinstance(value,dict):
                edited_dict[key] = {}
                for k,v in value.items():
                    if v != "":
                        edited_dict[key][k] = v
            else:
                edited_dict[key] = value

        candidate = self.client.watchlists.edit(ID, **edited_dict)

        candidate = candidate.body

        print("Edited candidate: ",candidate)

    # past hits of a candidate
    def past_hits(self, ID):

        listed = self.client.watchlists.search(ID)
        print(listed.body)


# in this function we are  getting inputs from user
def information_inputs():

    global note, birth_ISO, ssn, address_country_code, passport, first_name, last_name, address_street1,\
        address_street2, middle_name, address_city, address_subdivision, address_postal_code
    address_postal_code = None
    birth_ISO = input("birth date in ISO format*: ")
    ssn = input("ssn value*: ")
    passport = input("passport value*: ")
    first_name = input("First name*: ")
    middle_name = input("middle name: ")
    last_name = input("Last name*: ")
    address_street1 = input("address street1*: ")
    address_street2 = input("address street2: ")
    address_city = input("address city*: ")
    address_subdivision = input("address subdivision*: ")
    address_country_code = input("country code*: ")

    # address_postal_code is currently None but if the country has postal codes it will ask a postal code and
    #  overwrite it to the variable
    if address_country_code not in countries_without_ps:
        address_postal_code = input("postal code*: ")

    note = input("note: ")
    return note, birth_ISO,  ssn, passport, first_name, middle_name, last_name, address_street1, address_street2,address_city, address_subdivision, address_postal_code, address_country_code


def main():

    # creating our object
    user = Candidate()

    while True:
        action = input( " Type ' create ' to create a candidate, ' list ' to list candidates,"
                        " ' delete ' to delete a candidate, ' edit ' to edit a candidate,"
                        " ' hits 'to see the past hits of the candidate, 'quit' to close the application:" )

        try:

            if action == "create":
                user.create_candidate(*information_inputs())
            elif action == "list":
                user.list_candidates()

            elif action == "edit":
                ID = input("ID of the user you want to edit ")
                user.edit_candidate(ID,*information_inputs())

            elif action == "delete":
                ID = input("ID of the user you  want to delete ")
                user.delete_candidate(ID)

            elif action == "hits":
                ID = input("ID of the user you  want to see the past hits ")
                user.past_hits(ID)

            elif action == "quit":
                sys.exit(0)

            else:
                print('invalid action')
                sys.exit(1)

        # catching the invalid inputs
        except blockscore.error.ValidationError:
            print("invalid inputs")
            sys.exit(1)


if __name__ == "__main__":
    main()
