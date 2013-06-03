# -*- coding: utf-8 -*-
#
# String filtering.
#
# Author:Just van den Broecke

from util import Util
from filter import Filter
from packet import FORMAT

log = Util.get_log("stringfilter")

# Base class for any string filtering
class StringFilter(Filter):
    # Constructor
    def __init__(self, configdict, section, consumes, produces):
        Filter.__init__(self, configdict, section, consumes, produces)

    def invoke(self, packet):
        if packet.data is None:
            return packet
        return self.filter_string(packet)

    def filter_string(self, packet):
        pass

# String filtering using Python advanced String formatting
# String should have substitutable values like {schema} {foo}
# format_args should be of the form format_args = schema:test foo:bar ...
class StringSubstitutionFilter(StringFilter):
    # Constructor
    def __init__(self, configdict, section):
        StringFilter.__init__(self, configdict, section, consumes=FORMAT.string, produces=FORMAT.string)

        # Formatting of content according to Python String.format()
        # String should have substitutable values like {schema} {foo}
        # format_args should be of the form format_args = schema:test foo:bar ...
        self.format_args = self.cfg.get('format_args')

        # Convert string to dict: http://stackoverflow.com/a/1248990
        self.format_args_dict = Util.string_to_dict(self.format_args, ':')

    def filter_string(self, packet):
        # String substitution based on Python String.format()
        packet.data = packet.data.format(**self.format_args_dict)
        return packet



