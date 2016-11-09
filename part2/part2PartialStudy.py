# csci4211
# project3 part2

from pox.core import core
import pox.openflow.libopenflow_01 as of


# Even a simple usage of the logger is much nicer than print!
log = core.getLogger()


#use this table to add the needed entries
table = {}

# Handle messages the switch has sent us because it has no
# matching rule.

def _handle_PacketIn (event):
	
  
  # tell switch the future packet with dst = packet.src should automatically go event.port
  packet = event.parsed
  msg = of.ofp_flow_mod()
  msg.match.dl_dst = packet.src
  msg.actions.append(of.ofp_action_output(port = event.port))
  event.connection.send(msg)
  log.debug("Installing %s <-> %s" % (packet.src, packet.dst))
  # without using table {}
  # flood
  print "Implement >>> ", packet.src 
  msg = of.ofp_packet_out(data = event.ofp)
  msg.actions.append(of.ofp_action_output(port = of.OFPP_FLOOD))
  event.connection.send(msg)

def launch ():
  core.openflow.addListenerByName("PacketIn", _handle_PacketIn)
  log.info("Simple Routing Switch Running.")
