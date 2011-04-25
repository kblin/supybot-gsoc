###
# Copyright (c) 2011, Kai Blin
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
#   * Redistributions of source code must retain the above copyright notice,
#     this list of conditions, and the following disclaimer.
#   * Redistributions in binary form must reproduce the above copyright notice,
#     this list of conditions, and the following disclaimer in the
#     documentation and/or other materials provided with the distribution.
#   * Neither the name of the author of this software nor the name of
#     contributors to this software may be used to endorse or promote products
#     derived from this software without specific prior written consent.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED.  IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

###

import supybot.utils as utils
from supybot.commands import *
import supybot.plugins as plugins
import supybot.ircutils as ircutils
import supybot.callbacks as callbacks
from urllib import urlencode, urlopen

class Gsoc(callbacks.Plugin):
    """Provide some gsoc-specific commands that need to be more than just
       factoids"""
    threaded = True
    address = "http://kblin.org/code/gsoc_counter.php"

    def _increment_counter(self, factoid):
        """Increment the counter for a given factoid"""
        cookie = self.registryValue("secretCookie")
        query = [('factoid', factoid), ('cookie', cookie)]
        data = urlencode(query)
        urlopen(self.address, data)

    def next(self, irc, msg, args, redirect):
        """[<redirect>]

        trigger a query for the next event"""
        redir_str = (redirect is not None) and redirect or ""
        self._increment_counter("next")
        self.Proxy(irc.irc, msg, \
                   callbacks.tokenize("whatis next " + redir_str))
    next = wrap(next, [additional('text')])

    def countdown(self, irc, msg, args, redirect):
        """[<redirect>]

        get the countdown for the next event"""
        redir_str = (redirect is not None) and redirect or ""
        self._increment_counter("countdown")
        self.Proxy(irc.irc, msg, \
                   callbacks.tokenize("whatis countdown " + redir_str))
    countdown = wrap(countdown, [additional('text')])

Class = Gsoc


# vim:set shiftwidth=4 softtabstop=4 expandtab textwidth=79:
