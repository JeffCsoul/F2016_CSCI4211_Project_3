from pox.core import core
import pox.openflow.libopenflow_01 as of


# Even a simple usage of the logger is much nicer than print!
log = core.getLogger()


#use this table to add the needed entries
# key is (event.connection, host_MAC)
# value is the port number of a switch
table = {}



def _handle_PacketIn (event):
  packet = event.parsed

  # store or update the host's location via the incoming packet.
  # After completely studied, the size of table is the number of hosts
  table[(event.connection,packet.src)] = event.port
  # check if the controller has stored the port that points to destination host
  outputPort = table.get((event.connection,packet.dst))

  if outputPort is None:
    # controller does not know the destination
    msg = of.ofp_packet_out(data = event.ofp)
    msg.actions.append(of.ofp_action_output(port =  of.OFPP_FLOOD))
    event.connection.send(msg)
    log.debug("\nSwitch %s gets unknown destination  %s  <Flood operation>.", str(event.connection), str(packet.dst))
  else:
    # controller knows the destination
    # so it will set to forwarding entry to this switch, also ask the switch forward the packet to outputPort
    msg = of.ofp_flow_mod()
    msg.match.dl_dst = packet.src
    msg.match.dl_src = packet.dst
    msg.actions.append(of.ofp_action_output(port = event.port))
    event.connection.send(msg)
    
    
    msg = of.ofp_flow_mod()
    msg.data = event.ofp 
    msg.match.dl_src = packet.src
    msg.match.dl_dst = packet.dst
    msg.actions.append(of.ofp_action_output(port = outputPort))
    event.connection.send(msg)
    log.debug("\nSet switch %s two rules:", str(event.connection))
    log.debug("\n1. Send out these packets from host %s to host %s via port %s", str(packet.dst), str(packet.src), str(event.port))
    log.debug("\n2. Send out these packets from host %s to host %s via port %s", str(packet.src), str(packet.dst), str(outputPort))

def launch():
  core.openflow.addListenerByName("PacketIn", _handle_PacketIn)
  log.info("Simple Routing Switch Running.")

