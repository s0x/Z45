'''
Created on 06.01.2012

@author: Ivo Senner <ivo.senner@googlemail.com>
'''
import locale
import sys
import codecs
import logging
import string

from net.connection import Connection
from threading import Thread
from pyxmpp.all import JID,Iq,Presence,Message,StreamError
from pyxmpp.jabber.client import JabberClient
from pyxmpp.interface import implements
from pyxmpp.interfaces import IMessageHandlersProvider, IPresenceHandlersProvider
from pyxmpp.interfaces import IIqHandlersProvider, IFeaturesProvider
from pyxmpp.streamtls import TLSSettings
from pyxmpp.jabber.muc import MucRoomManager, MucRoomHandler
from pyxmpp.stanza import Stanza
from util.system_message import SystemMessage

class XmppConnection(Connection, Thread):
    '''
    classdocs
    '''

    def __init__(self, listener=None):
        '''
        Constructor
        '''
        Connection.__init__(self, listener)
        Thread.__init__(self);
        self.c = None
        
    def connect(self, username=None, password=None, server=None, channel=None, tls_cacerts = None):
        self.set_encoding()
        self.set_logging()
        
        print u"creating client..."
        # JID password ['tls_noverify'|cacert_file]
        self.c = Client(JID(username), password, tls_cacerts, channel)
        self.c.set_notify_msg_listener(self.notify_msg_listener)
        print u"connecting..."
        self.c.connect()
        self.start()
        
        return True

    def run(self):
        self.c.loop(1)
    
    def disconnect(self):
        self.c.disconnect()
        return True
    
    def send(self, msg):
        self.c.stream.send(msg.get_source() + u": " + msg.get_body())
        return True
    
    def set_encoding(self):
        # XMPP protocol is Unicode-based to properly display data received
        # _must_ convert it to local encoding or UnicodeException may be raised
        locale.setlocale(locale.LC_CTYPE, "")
        encoding = locale.getlocale()[1]
        if not encoding:
            encoding = "us-ascii"
        sys.stdout = codecs.getwriter(encoding)(sys.stdout, errors = "replace")
        sys.stderr = codecs.getwriter(encoding)(sys.stderr, errors = "replace")

    def set_logging(self):
        # PyXMPP uses `logging` module for its debug output
        # applications should set it up as needed
        logger = logging.getLogger()
        logger.addHandler(logging.StreamHandler())
        logger.setLevel(logging.INFO) # change to DEBUG for higher verbosity


class Client(JabberClient):
    '''
    Simple bot (client) example. Uses `pyxmpp.jabber.client.JabberClient`
    class as base. That class provides basic stream setup (including
    authentication) and Service Discovery server. It also does server address
    and port discovery based on the JID provided.
    '''
    
    def __init__(self, jid, password, tls_cacerts, channel):
        self.notify_msg_listener = None
        self.channel = channel;
        # if bare JID is provided add a resource -- it is required
        if not jid.resource:
            jid=JID(jid.node, jid.domain, "Echobot")

        if tls_cacerts:
            if tls_cacerts == 'tls_noverify':
                tls_settings = TLSSettings(require = True, verify_peer = False)
            else:
                tls_settings = TLSSettings(require = True, cacert_file = tls_cacerts)
        else:
            tls_settings = None
            
        # setup client with provided connection information
        # and identity data
        JabberClient.__init__(self, jid, password,
                disco_name="Datenverarbeitungseinheit Z45", disco_type="z45",
                tls_settings = tls_settings)

        # add the separate components
        self.interface_providers = [
            VersionHandler(self),
            EchoHandler(self),
            ]
        
    def set_notify_msg_listener(self, notify_msg_listener):
        self.notify_msg_listener
    
    def session_started(self):
        """Handle session started event. May be overriden in derived classes. 
        This one requests the user's roster and sends the initial presence.""" 
        print u'SESSION STARTED'
        self.request_roster() 
        p=Presence() 
        self.stream.send(p) 
        print u'ConnectToParty'
        self.connectToMUC()
    
    def connectToMUC(self):
        self.roomManager = MucRoomManager(self.stream);
        channel_el = string.split(self.channel, "@")
        self.roomHandler = ChatHandler(JID(channel_el[0], channel_el[1], "z45"), self.notify_msg_listener)
        self.roomState = self.roomManager.join(
        room=JID(self.channel),
        nick='z45',
        handler=self.roomHandler, 
        history_maxchars=0,
        password = None)
        self.roomManager.set_handlers()
        self.roomState.send_message("Sending this Message")
        
        
    def stream_state_changed(self,state,arg):
        '''
        This one is called when the state of stream connecting the component
        to a server changes. This will usually be used to let the user
        know what is going on.
        '''
        print "*** State changed: %s %r ***" % (state,arg)

    def print_roster_item(self,item):
        if item.name:
            name=item.name
        else:
            name=u""
        print (u'%s "%s" subscription=%s groups=%s'
                % (unicode(item.jid), name, item.subscription,
                    u",".join(item.groups)) )

    def roster_updated(self,item=None):
        if not item:
            print(u"My roster:")
            for item in self.roster.get_items():
                self.print_roster_item(item)
            return
        print u"Roster item updated:"
        self.print_roster_item(item)

class ChatHandler(MucRoomHandler):
    
    def __init__(self, jid, notify_msg_listener = None):
        MucRoomHandler.__init__(self)
        self.notify_msg_listener = notify_msg_listener
        self.jid = jid
    
    def user_joined(self, user, stanza):
        MucRoomHandler.user_joined(self, user, stanza)
        
    def user_left(self, user, stanza):
        MucRoomHandler.user_left(self, user, stanza)
        
    def role_changed(self, user, old_role, new_role, stanza):
        MucRoomHandler.role_changed(self, user, old_role, new_role, stanza)
        
    def nick_changed(self, user, old_nick, stanza):
        MucRoomHandler.nick_changed(self, user, old_nick, stanza)
        
    def subject_changed(self, user, stanza):
        MucRoomHandler.subject_changed(self, user, stanza)
        #msg = Sy
        
    def message_received(self, user, stanza):
        MucRoomHandler.message_received(self, user, stanza)
        print str(user.room_jid)
        if self.jid != user.room_jid:
            msg = Message(user.nick, user.room_jid.node+'@'+user.room_jid.domain, stanza.get_body())
            print(str(msg))
            self.notify_msg_listener(msg)
    pass

class EchoHandler(object):
    """Provides the actual 'echo' functionality.

Handlers for presence and message stanzas are implemented here.
"""

    implements(IMessageHandlersProvider, IPresenceHandlersProvider)
    
    def __init__(self, client):
        """Just remember who created this."""
        self.client = client
    
    def get_message_handlers(self):
        """Return list of (message_type, message_handler) tuples.

The handlers returned will be called when matching message is received
in a client session."""
        return [
            ("normal", self.message),
            ]

    def get_presence_handlers(self):
        """
        Return list of (presence_type, presence_handler) tuples.
        The handlers returned will be called when matching presence stanza is
        received in a client session.
        """
        return [
            (None, self.presence),
            ("unavailable", self.presence),
            ("subscribe", self.presence_control),
            ("subscribed", self.presence_control),
            ("unsubscribe", self.presence_control),
            ("unsubscribed", self.presence_control),
            ]

    def message(self,stanza):
        """Message handler for the component.

Echoes the message back if its type is not 'error' or
'headline', also sets own presence status to the message body. Please
note that all message types but 'error' will be passed to the handler
for 'normal' message unless some dedicated handler process them.

:returns: `True` to indicate, that the stanza should not be processed
any further."""
        subject=stanza.get_subject()
        body=stanza.get_body()
        t=stanza.get_type()
        print u'Message from %s received.' % (unicode(stanza.get_from(),)),
        if subject:
            print u'Subject: "%s".' % (subject,),
        if body:
            print u'Body: "%s".' % (body,),
        if t:
            print u'Type: "%s".' % (t,)
        else:
            print u'Type: "normal".'
        if stanza.get_type()=="headline":
            # 'headline' messages should never be replied to
            return True
        if subject:
            subject=u"Re: "+subject
        m=Message(
            to_jid=stanza.get_from(),
            from_jid=stanza.get_to(),
            stanza_type=stanza.get_type(),
            subject=subject,
            body=body)
        if body:
            p = Presence(status=body)
            return [m, p]
        return m

    def presence(self,stanza):
        """Handle 'available' (without 'type') and 'unavailable' <presence/>."""
        msg=u"%s has become " % (stanza.get_from())
        t=stanza.get_type()
        if t=="unavailable":
            msg+=u"unavailable"
        else:
            msg+=u"available"

        show=stanza.get_show()
        if show:
            msg+=u"(%s)" % (show,)

        status=stanza.get_status()
        if status:
            msg+=u": "+status
        print msg

    def presence_control(self,stanza):
        """Handle subscription control <presence/> stanzas -- acknowledge
        them."""
        msg=unicode(stanza.get_from())
        t=stanza.get_type()
        if t=="subscribe":
            msg+=u" has requested presence subscription."
        elif t=="subscribed":
            msg+=u" has accepted our presence subscription request."
        elif t=="unsubscribe":
            msg+=u" has canceled his subscription of our."
        elif t=="unsubscribed":
            msg+=u" has canceled our subscription of his presence."

        print msg

        return stanza.make_accept_response()


class VersionHandler(object):
    """Provides handler for a version query.
    This class will answer version query and announce 'jabber:iq:version' namespace
    in the client's disco#info results."""
    implements(IIqHandlersProvider, IFeaturesProvider)

    def __init__(self, client):
        """Just remember who created this."""
        self.client = client

    def get_features(self):
        """Return namespace which should the client include in its reply to a
disco#info query."""
        return ["jabber:iq:version"]

    def get_iq_get_handlers(self):
        """Return list of tuples (element_name, namespace, handler) describing
handlers of <iq type='get'/> stanzas"""
        return [
            ("query", "jabber:iq:version", self.get_version),
            ("query", "jabber:iq:version", self.get_version),
            ]

    def get_iq_set_handlers(self):
        """Return empty list, as this class provides no <iq type='set'/> stanza handler."""
        return []

    def get_version(self,iq):
        """Handler for jabber:iq:version queries.

        jabber:iq:version queries are not supported directly by PyXMPP, so the
        XML node is accessed directly through the libxml2 API. This should be
        used very carefully!"""
        iq=iq.make_result_response()
        q=iq.new_query("jabber:iq:version")
        q.newTextChild(q.ns(),"name","Datenverarbeitungseinheit Z45")
        q.newTextChild(q.ns(),"version","Version 22.06.1910")
        return iq
