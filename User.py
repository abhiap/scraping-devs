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
    user.set('username', 'Abhi2@gh')
    user.set('name', 'Abhijit')
    user.set('email', "ab@cd.com")
    print(user)
    print(user.variables)
    print(user.get("username"), user.get('name'), user.get("email"))


if __name__ == '__main__': main()
