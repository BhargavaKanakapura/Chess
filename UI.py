import constants

class IvalidLogin(Exception):
    def __init__(self, uop):
        self.message = "INVALID LOGIN --> " + uop.upper() + " IVALID"
        super().__init__(self.message)

class IvalidInput(Exception):
    def __init__(self, text_field):
        self.message = "INVALID INPUT FOR " + text_field
        super().__init__(self.message)

def valid_login(username, password):

    username = hash(username)

    try:
        if constants.LOGINS[username] == password: return True
        else: raise IvalidLogin("PASSWORD")

    except KeyError:
        raise IvalidLogin("USERNAME")