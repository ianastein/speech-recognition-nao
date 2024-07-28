import qi
import sys 

class Authenticator:

    def __init__(self, username, password):
        self.username = "nao"
        self.password = "nao6_1ki"

    # This method is expected by libqi and must return a dictionary containing
    # login information with the keys 'user' and 'token'.
    def initialAuthData(self):
        return {'user': self.username, 'token': self.password}

class AuthenticatorFactory:

    def __init__(self, username, password):
        self.username = username
        self.password = password

    # This method is expected by libqi and must return an object with at least
    # the `initialAuthData` method.
    def newAuthenticator(self):
        return Authenticator(self.username, self.password)

def getConnection() :
    app = qi.Application(sys.argv, url="tcp://192.168.171.148:9559")
    logins = ("nao", "OMITTED")
    factory = AuthenticatorFactory(*logins)
    app.session.setClientAuthenticatorFactory(factory)
    app.start()
    print("NAO ROBOT SUCCESSFULLY CONNECTED !!!")
    return app
