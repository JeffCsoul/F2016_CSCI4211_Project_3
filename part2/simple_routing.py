from pox.core import core
import pox.openflow.libopenflow_01 as of


# Even a simple usage of the logger is much nicer than print!
log = core.getLogger()


#use this table to add the needed entries
table = {}

# Handle messages the switch has sent us because it has no
# matching rule.

def _handle_PacketIn (event):
  # check if the entry is in the table or not
  # if it's not in the table, add an entry to the table
  # We don't know where the destination is yet.  So, we'll just
  # send the packet out all ports (except the one it came in on!)
  # and hope the destination is out there somewhere. :)
  # To send out all ports, we can use either of the special ports
  # OFPP_FLOOD or OFPP_ALL. 
  # if the appropriate entry is in the table, just forward the packet to that port

def launch ():
  core.openflow.addListenerByName("PacketIn", _handle_PacketIn)
  log.info("Simple Routing Switch Running.")
