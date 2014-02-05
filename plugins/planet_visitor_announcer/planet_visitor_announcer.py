from base_plugin import BasePlugin
from packets import warp_command
from twisted.internet import reactor

class PlanetVisitorAnnouncer(BasePlugin):
    """
    Broadcasts a message whenever a player joins or leaves the server.
    """
    name = "planet_visitor_announcer_plugin"
    auto_activate = True

    def activate(self):
        super(PlanetVisitorAnnouncer, self).activate()

    def after_warp_command(self, data):
        w = warp_command().parse(data.data)
        if w.warp_type == "WARP_DOWN" or w.warp_type == "WARP_HOME":
            print "before later: I (%s) am on: %s" % (self.protocol.player.name, self.protocol.player.planet)
            reactor.callLater(1, self.check_planet, self.protocol.player)

    def check_planet(self, who_beamed):
            print "later: I (%s) am on: %s" % (who_beamed.name, who_beamed.planet)
            for protocol in self.protocol.factory.protocols.itervalues():
                print "%s is on: %s" % (protocol.player.name, protocol.player.planet)
                if protocol.player.planet == self.protocol.player.planet and protocol.player is not who_beamed:
                    print "sending a notification to %s" % protocol.player.name
                    protocol.send_chat_message(
                        "%s beamed down to your planet" % who_beamed.colored_name(self.config.colors)
                    )

