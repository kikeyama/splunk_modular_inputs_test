# $SPLUNK_HOME/etc/apps/hello_mi/bin/hello.py

import sys
import xml.dom.minidom, xml.sax.saxutils
import logging

#set up logging suitable for splunkd comsumption
logging.root
logging.root.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(levelname)s %(message)s')
handler = logging.StreamHandler()
handler.setFormatter(formatter)
logging.root.addHandler(handler)

SCHEME = """<scheme>
    <title>Slack</title>
    <description>Get data from Slack.</description>
    <use_external_validation>true</use_external_validation>
    <streaming_mode>simple</streaming_mode>
    <endpoint>
        <args>
            <arg name="name">
                <title>Slack Domain Name</title>
                <description>Name of the domain name of Slack (e.g. example.slack.com).</description>
            </arg>
            <arg name="token">
                <title>Token</title>
                <description>Slack API Token</description>
            </arg>
        </args>
    </endpoint>
</scheme>
"""

# Empty introspection routine
def do_scheme(): 
    print SCHEME

# Empty validation routine. This routine is optional.
def validate_arguments(): 
    pass

# Routine to get the value of an input
def get_who(): 
    try:
        # read everything from stdin
        config_str = sys.stdin.read()

        # parse the config XML
        doc = xml.dom.minidom.parseString(config_str)
        root = doc.documentElement
        conf_node = root.getElementsByTagName("configuration")[0]
        if conf_node:
            stanza = conf_node.getElementsByTagName("stanza")[0]
            if stanza:
                stanza_name = stanza.getAttribute("name")
                if stanza_name:
                    params = stanza.getElementsByTagName("param")
                    for param in params:
                        param_name = param.getAttribute("name")
                        if param_name and param.firstChild and \
                            param.firstChild.nodeType == param.firstChild.TEXT_NODE and \
                            param_name == "who":
                            return param.firstChild.data
    except Exception, e:
        raise Exception, "Error getting Splunk configuration via STDIN: %s" % str(e)

    return ""

# Routine to index data
def run_script(): 
    print "hello world, %s!" % get_who()

# Script must implement these args: scheme, validate-arguments
if __name__ == '__main__':
    if len(sys.argv) > 1:
        if sys.argv[1] == "--scheme":
            do_scheme()
        elif sys.argv[1] == "--validate-arguments":
            validate_arguments()
        else:
            pass
    else:
        run_script()

    sys.exit(0)
