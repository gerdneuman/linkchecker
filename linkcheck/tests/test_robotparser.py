# -*- coding: iso-8859-1 -*-
# Copyright (C) 2004  Bastian Kleineidam
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 675 Mass Ave, Cambridge, MA 02139, USA.

import unittest

import linkcheck.robotparser2


class TestRobotParser (unittest.TestCase):
    """test robots.txt parser (needs internet access)"""

    def setUp (self):
        """initialize self.rp as a robots.txt parser"""
        self.rp = linkcheck.robotparser2.RobotFileParser()

    def check (self, a, b):
        """helper function comparing two results a and b"""
        if not b:
            ac = "access denied"
        else:
            ac = "access allowed"
        if a != b:
            self.fail("%s != %s (%s)" % (a, b, ac))

    def test_existing_robots (self):
        """test parsing and access of an existing robots.txt file"""
        # robots.txt that exists, gotten to by redirection
        self.rp.set_url('http://www.musi-cal.com/robots.txt')
        self.rp.read()
        # test for re.escape
        self.check(self.rp.can_fetch('*', 'http://www.musi-cal.com/'), True)
        # this should match the first rule, which is a disallow
        self.check(self.rp.can_fetch('', 'http://www.musi-cal.com/'), False)
        # various cherry pickers
        self.check(self.rp.can_fetch('CherryPickerSE',
                           'http://www.musi-cal.com/cgi-bin/event-search'
                           '?city=San+Francisco'), False)
        self.check(self.rp.can_fetch('CherryPickerSE/1.0',
                           'http://www.musi-cal.com/cgi-bin/event-search'
                           '?city=San+Francisco'), False)
        self.check(self.rp.can_fetch('CherryPickerSE/1.5',
                           'http://www.musi-cal.com/cgi-bin/event-search'
                           '?city=San+Francisco'), False)
        # case sensitivity
        self.check(self.rp.can_fetch('ExtractorPro',
                                     'http://www.musi-cal.com/blubba'), False)
        self.check(self.rp.can_fetch('extractorpro',
                                     'http://www.musi-cal.com/blubba'), False)
        # substring test
        self.check(self.rp.can_fetch('toolpak/1.1',
                                     'http://www.musi-cal.com/blubba'), False)
        # tests for catch-all * agent
        self.check(self.rp.can_fetch('spam',
                                    'http://www.musi-cal.com/vsearch'), False)
        self.check(self.rp.can_fetch('spam',
                                 'http://www.musi-cal.com/Musician/me'), True)
        self.check(self.rp.can_fetch('spam',
                                     'http://www.musi-cal.com/'), True)
        self.check(self.rp.can_fetch('spam',
                                     'http://www.musi-cal.com/'), True)

    def test_nonexisting_robots (self):
        """test access of a non-existing robots.txt file"""
        # robots.txt that does not exist
        self.rp.set_url('http://www.lycos.com/robots.txt')
        self.rp.read()
        self.check(self.rp.can_fetch('Mozilla',
                                     'http://www.lycos.com/search'), True)


def test_suite ():
    """build and return a TestSuite"""
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestRobotParser))
    return suite

if __name__ == '__main__':
    unittest.main()
