class User(object):
    """__init__() functions as the class constructor"""
    def __init__(self, **kwargs):
        self.variables = kwargs

    def set(self, k, v):
        self.variables[k] = v

    def get(self, k):
        return self.variables.get(k, None)

# class Person(object):
#     """__init__() functions as the class constructor"""
#     def __init__(self, name=None, job=None, quote=None):
#         self.name = name
#         self.job = job
#         self.quote = quote

def main():
    user = User()
    user.set('Username', 'Abhi2@gh')
    user.set('Name', 'Abhijit')
    user.set('Email', "ab@cd.com")
    print(user)
    print(user.variables)
    print(user.variables.keys())
    print(user.get("Username"), user.get('Name'), user.get("Email"))


if __name__ == '__main__': main()
