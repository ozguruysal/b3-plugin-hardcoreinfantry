# -*- encoding: utf-8 -*-

def prepare_fakeparser_for_tests():
    from b3.fake import fakeConsole, FakeConsole

    class Frostbite2_connection():
        connected = True

    p = Frostbite2_connection()
    FakeConsole._serverConnection = p

    def frostbitewrite(self, msg, maxRetries=1, needConfirmation=False):
        """send text to the console"""
        if type(msg) == str:
            # console abuse to broadcast text
            self.say(msg)
        elif type(msg) == tuple:
            print "   >>> %s" % repr(msg)
            if len(msg) >= 4 and msg[0] == 'admin.movePlayer':
                client = getClient(self, msg[1])
                if client:
                    client.teamId = int(msg[2])
                    client.squad = int(msg[3])

    FakeConsole.write = frostbitewrite