from jnpr.junos.utils.config import Config
from jnpr.junos import Device
import jinja2

# This function loads the configuration entered in the webpage to a template and returns the "show | compare"
# Uses vrf-template.conf
def input_conf(host, user, password, post):
    global conf
    global dev
    dev = Device(host=host,user=user,password=password,gather_facts=False)
    conf = Config(dev)
    dev.open()
    vrf_vars = {
        'if_ip' : str(post['if_ip']),
        'vrf_name' : str(post['vrf_name']),
        'if_phy' : str(post['if_phy']),
        'if_vlan' : str(post['if_vlan']),
        'route_distinguisher' : str(post['route_distinguisher']),
        'vrf_target' : str(post['vrf_target']),
        'bgp_group' : str(post['bgp_group']),
        'bgp_as' : str(post['bgp_as']),
        'bgp_neighbor' : str(post['bgp_neighbor'])
    }
    conf.load(template_path='cfgdev/vrf-template.conf',template_vars=vrf_vars,merge=True)
    showcompare = conf.diff()
    return showcompare

# Commits the configuration
def cfgcommit():
    global conf
    global dev
    conf.commit()
    dev.close()
    return

# Rollback the configuration
def cfgrollback():
    global conf
    global dev
    conf.rollback()
    dev.close()
    return

