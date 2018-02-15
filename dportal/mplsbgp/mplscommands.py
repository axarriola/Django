import yaml
import string
from collections import defaultdict
from jnpr.junos import Device
from jnpr.junos.factory.factory_loader import FactoryLoader

# YAML string instead of file
yml = '''
---
mplsLSPs:
 rpc: get-mpls-lsp-information
 args_key: regex
 args: 
  extensive: True
  ingress: True
  count_active_routes: True
 item: rsvp-session-data/rsvp-session/mpls-lsp
 key: name
 view: mplsView

mplsView:
 fields:
  destination_address: destination-address
  lsp_state: lsp-state
  route_count: { route-count : int }
  active_path: active-path
  lsp_path: _lspPathTable

_lspPathTable:
  item: mpls-lsp-path
  key: name
  view: _lspPathView

_lspPathView:
  fields:
   path_name: name
   path_title: title
   path_active: { path-active : flag }
   path_state: path-state
   admin_groups: admin-groups/admin-group-name
   path_ero: explicit-route/address
   path_rro: received-rro

rsvpSessions:
 rpc: get-rsvp-session-information
 args_key: session-name
 args: 
  extensive: True
  ingress: True
 item: rsvp-session-data/rsvp-session
 key: name
 view: rsvpSessionView

rsvpSessionView:
 fields:
  lsp_path_type: lsp-path-type
  lsp_state: lsp-state
  lsp_id: lsp-id
  tunnel_id: tunnel-id
  is_nodeprotection: { is-nodeprotection : flag }
  bypass_name: bypass-name
  is_fastreroute: { is-fastreroute : flag }
  detour_state: detour/lsp-state
  detour_ero: detour/explicit-route/address
  detour_rro: detour/record-route/address
'''

#This function is used by the view to obtain the MPLS/RSVP information and display it.
def get_mpls_info(host, user, password, regex, lsys):
    # Load the classes created by the FactoryLoader with the YAML to the global variables so they can be referenced 
    globals().update(FactoryLoader().load(yaml.load(yml)))
    dev = Device(host=host, user=user, password=password, gather_facts=False)
    dev.open()
    if lsys:
        if(regex.isspace() or regex == ""):
            ml = mplsLSPs(dev).get(logical_system=str(lsys))
            rs = rsvpSessions(dev).get(logical_system=str(lsys))
        else:
            ml = mplsLSPs(dev).get(str(regex), logical_system=str(lsys))
            rs = rsvpSessions(dev).get(str(regex), logical_system=str(lsys))
    else:
        if(regex.isspace() or regex == ""):
            ml = mplsLSPs(dev).get()
            rs = rsvpSessions(dev).get()
        else:
            ml = mplsLSPs(dev).get(str(regex))
            rs = rsvpSessions(dev).get(str(regex))

    dev.close()
    
    # Move all rsvpSessions information to a defaultdict. We need to be able to get
    # rsvp sessions information with the LSP name as key. Normally there is more
    # than 1 rsvp session with the same name, so to get all the sessions in the original
    # "dict" (OpTable.rsvpSessions) we would have to iterate through it searching
    # for each sessions called the same as the LSP, for every LSP. This way we do it
    # all at once, one iteration instead of N (#LSPs) iterations.
    rsvp_sessions = defaultdict(list)
    for rskey in rs.keys():
        rsvp_sessions[rskey].append(rs[rskey])

    #Prepare the string with the information structured as we need it to be displayed in the webpage   
    output = ""  
    for item in ml:
        output += "\nName: "+item.name + "    To: "+ item.destination_address + "    State: "+item.lsp_state+ "\n"
        output += "Route Count: " + str(item.route_count) + "        Active Path: " + item.active_path+ "\n"
        output +=  "\nPaths: "+ "\n"
        for path in item.lsp_path:
            output += "\nPath: "+path.path_name+" ("+path.path_title+")"
            if path.path_active:
                output += "* "
            output += "Include:" + string.translate(str(path.admin_groups),None,"'")+ "\n"
            output += "ERO: " + string.translate(str(path.path_ero),None,"'") + "\n"
            if path.path_rro:
                output += path.path_rro + "\n"
        output += "\nRSVP info: " + " \n "
        
        rsvp_sessionslsp = rsvp_sessions[item.name]
        for rsvp_session in rsvp_sessionslsp:
            output += "\nPath: "+rsvp_session.lsp_path_type+"    State: "+rsvp_session.lsp_state + "\n"
            output += "LSP ID: "+rsvp_session.lsp_id+"      Tunnel ID: "+rsvp_session.tunnel_id + "\n"
            if rsvp_session.is_nodeprotection:
                if rsvp_session.bypass_name:
                    output += "Using: " + rsvp_session.bypass_name + "\n"
                else:
                    output += "Node-link protection desired. No bypass selected.\n" 
            if rsvp_session.is_fastreroute:
                if rsvp_session.detour_state:
                    output += "FRR:" + "\n"
                    output += "Detour State: " + rsvp_session.detour_state + "\n"
                    output += "ERO: " + str(rsvp_session.detour_ero) + "\n"
                    output += "RRO: " + str(rsvp_session.detour_rro) + "\n"
                else:
                    output += "FRR protection desired. Detour not established.\n" 
        output += "------------------------------------------------------------------------------------------" + " \n "

    return output
