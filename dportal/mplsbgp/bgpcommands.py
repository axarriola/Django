import yaml
from jnpr.junos import Device
from jnpr.junos.factory.factory_loader import FactoryLoader

# Instead of loading a YAML-file place it within the code
yml = '''
---
bgpRoutes:
 rpc: get-route-information
 args:
  protocol: bgp 
  detail: True
 item: route-table/rt
 key: rt-destination
 view: bgpView

bgpView:
 fields:
  as_path: rt-entry/as-path
  rt_destination: rt-destination
  rt_prefix_length: rt-prefix-length
  preference: rt-entry/preference
  community: rt-entry/communities/community
'''

#This function is used by the view to obtain the BGP information and display it.
def get_bgp_routes(host,user,password,route,lsys):
    # Load the classes created by the FactoryLoader with the YAML to the global variables so they can be referenced
    globals().update(FactoryLoader().load(yaml.load(yml)))
    dev = Device(host=host, user=user, password=password, gather_facts=False)
    dev.open()
    dev.timeout = 60
    if lsys:
        if(route.isspace() or route == ""):
            bt = bgpRoutes(dev).get(active_path=True,
                                table="inet.0", logical_system=str(lsys))
        else:
            bt = bgpRoutes(dev).get(active_path=True, destination=str(route),
                                table="inet.0", logical_system=str(lsys))
    else:
        if(route.isspace() or route == ""):
            bt = bgpRoutes(dev).get(active_path=True,
                                table="inet.0")
        else:
            bt = bgpRoutes(dev).get(active_path=True, destination=str(route),
                                table="inet.0")
    #Prepare the string with the information structured as we need it to be displayed
    output = ""
    for item in bt:
        output += "\n-\n"
        output += ("Route: "+item.rt_destination+"/"+item.rt_prefix_length+"\n")
        output += (item.as_path+" // Preference: "+item.preference+" // Community: "+str(item.community)+"\n")
    output += ("-\n")
    #output += ("---------------------------------------------\n")

    dev.close()
    return output
