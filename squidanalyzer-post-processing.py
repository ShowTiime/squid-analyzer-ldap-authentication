#!/usr/bin/env python

import re
import ldap
import ldif
import sys

address = '$SERVER_LDAP_IP'
user = '$USER@$COMPLETE_DOMAIN'
password = '$PASSWORD'
base1 = "cn=Users, dc=$DOMAIN, dc=$SUB_DOMAIN"
base2 = "ou=Admins, dc=$DOMAIN, dc=$SUB_DOMAIN"

conn = ldap.initialize('ldap://' + address)
conn.protocol_version = 3
conn.set_option(ldap.OPT_REFERRALS, 0)
conn.simple_bind_s(user, password)

resultados1 = conn.search_s(base1, ldap.SCOPE_SUBTREE, '(displayName=*)', ['displayName', 'cn'])
resultados2 = conn.search_s(base2, ldap.SCOPE_SUBTREE, '(displayName=*)', ['displayName', 'cn'])

userAliases = {}
for i in resultados1:
  cn = i[1]['cn'][0]
  if (cn.isdigit()):
    userAliases[i[1]['cn'][0]] = i[1]['displayName'][0]

for i in resultados2:
  cn = i[1]['cn'][0]
  if (cn.isdigit()):
    userAliases[i[1]['cn'][0]] = i[1]['displayName'][0]

# HTML and REGEX code to create a new column in SquidAnalyzer UI
column = "Login</th>\n<th>Users</th>"
columnregex = r"Users</th>"

# HTML and REGEX code to create and add elements to the table in SquidAnalyzer UI
login = "</a></td>\n<td><a>NOME-AQUI</a></td>"
loginregex = r"</a></td>\n"
loginNameRegex = r"NOME-AQUI"

# Taking user.html file from SquidAnalyzer and adding to the html variable
arq = open('/var/www/squidanalyzer/2019/user.html', 'r')
html = arq.read()
arq.close()

# Verifying the post-processing necessity
test_login_regex = r"Login</th>"
if (not re.search(test_login_regex, html)):

  # Localizing and substituting the HTML code to create the new table's column
  html = re.sub(loginregex, login, html)
  html = re.sub(columnregex, column, html)
  
  # Updatind the test file html.html
  arq = open('/var/www/html.html', 'w')
  arq.write(html)
  arq.close()
  
  # Opening html.html file and separating the lines
  arq = open('/var/www/html.html', 'r')
  html = arq.readlines()
  arq.close()
  
  for code in range(len(html)):
    html[code] = html[code].rstrip('\n')
  
  newHTML = []
  i = 0
  
  for linha in html:
    if (linha == '<td><a>NOME-AQUI</a></td>'):
      title = html[i - 1].split('>')[2].split('<')[0]
      name = userAliases.get(title, 'not in domain')
      newHTML.append('<td><a>' + name + '</a></td>\n')
    else:
      newHTML.append(linha + '\n')
    i += 1
  
  arq = open('/var/www/squidanalyzer/2019/user.html', 'w')
  arq.writelines(newHTML)
  arq.close()
