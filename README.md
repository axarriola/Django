# Django Test
This small project was made as a sample of what can be done combining Django and Junos-pyez library. The focus was more on the backend, not much fancy html or any css, if you want to add a bit more of visual to it you can visit getbootstrap.com to easily add some more html and css to it.

It has two apps:


# MPLS/BGP
You may choose to query MPLS or BGP information from a device (whose information is saved in the database). For the MPLS, you enter an LSP regex and it will display the MPLS and RSVP information of all the LSPs. Regarding the BGP, you can enter a host IP or a subnet, and it will display all the matched subnets in a summarized way with information like communities, which normally is not displayed in a brief output.

# Configure Device
Choose a device from the database and enter configuration information for a VRF. It will display the "show | compare" and ask to commit or rollback.

