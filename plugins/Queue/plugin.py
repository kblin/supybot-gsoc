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


class Queue(callbacks.Plugin):
    """A simple queue manager for meetings."""
    _queue = []

    def queue(self, irc, msg, args, notice):
        """[<notice>]

        Queue up for saying something at the meeting, with an optional notice
        """
        self._queue.append((msg.nick, notice))
        irc.reply("I queued you at position %s in the queue" % len(self._queue))
    queue = wrap(queue, [additional('text')])

    def showqueue(self, irc, msg, args):
        """Show the current queue"""
        if len(self._queue) == 0:
            irc.reply("The queue is empty", private=True)
            return
        i = 1
        for nick, notice in self._queue:
            response = "%02d. %s" % (i, nick)
            if notice is not None:
                response += " %s" % notice
            irc.reply(response, private=True)
            i += 1
            if i > 10:
                irc.reply("... and more ...", private=True)
                break
    showqueue = wrap(showqueue)

    def nextinline(self, irc, msg, args):
        """Show the next person in line"""
        if len(self._queue) > 0:
            nick, notice = self._queue.pop(0)
            response = "Next in line is %s" % nick
            if notice is not None:
                response += " with notice '%s'" % notice
            irc.reply(response)
        else:
            irc.reply("There's nobody queued up right now.")
    nextinline = wrap(nextinline, ["owner"])


Class = Queue


# vim:set shiftwidth=4 softtabstop=4 expandtab textwidth=79:
