# SquidAnalyzer LDAP Authentication

This script must be executed after squid-analyzer. Its main function is to be a postprocessing script that takes all usernames from the SquidAnalyzer UI, connects to the LDAP Server, gets all matching names for each username and modifies the SquidAnalyzer UI to show you all the users' names and usernames.

## How To?

You only need to replace the corresponding $VARIABLES with the appropriate values.

* $SERVER_LDAP_IP = Your LDAP Server's IP (e.g. '192.168.1.2')
* $USER = Your username in the domain (e.g. 'show.tiime')
* $COMPLETE_DOMAIN = Your domain's name (e.g. 'local.domain.com')
* $PASSWORD = Your current password in the domain (e.g. 'test123')
* $DOMAIN = Part of the domain's name (e.g. 'local')
* $SUB_DOMAIN = Another parts of the domains names (e.g. 'domain')

> In the variables **base1** and **base2** you can add how many subdomains you have. I'll give you a example. My domain is 'local.domain.com' and the CN 'Users' contain all the network users. So, my variable **base1** will be like:
>  
> base1 = "cn=Users, dc=local, dc=domain, dc=com"
 
