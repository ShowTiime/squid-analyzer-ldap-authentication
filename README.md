# SquidAnalyzer LDAP Authentication

This script must be executed after squid-analyzer. Its main function is to be a postprocessing script that takes all usernames from the SquidAnalyzer UI, connects to the LDAP Server, gets all matching names for each username and modifies the SquidAnalyzer UI to show you all the users' names and usernames.
