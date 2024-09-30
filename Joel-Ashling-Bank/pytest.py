import random

def generate_username(firstname, lastname):
    get_firstname = firstname[:3]
    get_lastname = lastname[:3]

    value_length = 3
    value_string = "0123456789"
    username = get_firstname + get_lastname+"".join(random.sample(value_string, k=value_length))
    print(username)


firstname = input("Enter your firstname")
lastname = input("Enter your lastname")
generate_username(firstname,lastname)