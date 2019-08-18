#!/usr/bin/env python

import re
import ldap
import ldif
import sys

address = '$SERVER_LDAP_IP'
user = '$USER@$DOMAIN'
password = '$PASSWORD'
base1 = "cn=Users, dc=$DOMAIN, dc=$SUB_DOMAIN"
# base2 = "ou=Admins, dc=$DOMAIN, dc=$SUB_DOMAIN""

conn = ldap.initialize('ldap://' + address)
conn.protocol_version = 3
conn.set_option(ldap.OPT_REFERRALS, 0)
conn.simple_bind_s(user, password)

resultados1 = conn.search_s(base1, ldap.SCOPE_SUBTREE, '(displayName=*)', ['displayName', 'cn'])
# resultados2 = conn.search_s(base2, ldap.SCOPE_SUBTREE, '(displayName=*)', ['displayName', 'cn'])

userAliases = {}
for i in resultados1:
  cn = i[1]['cn'][0]
  if (cn.isdigit()):
    userAliases[i[1]['cn'][0]] = i[1]['displayName'][0]

for i in resultados2:
  cn = i[1]['cn'][0]
  if (cn.isdigit()):
    userAliases[i[1]['cn'][0]] = i[1]['displayName'][0]

#def findTitle(name, nameToTitle):
#  for i in range(len(nameToTitle)):
#    if (name == nameToTitle[i][0]):
#      return nameToTitle[i][1]
#  return 'title'

#Carregando arquivo Nome->Titulo
#nameToTitle = []

#file = open('/etc/squidanalyzer/user-aliases', 'r')
#userAliases = file.readlines()
#file.close()

#for i in range(len(userAliases)):
#  userAliases[i] = userAliases[i].rstrip('\n')

#for i in userAliases:
#  nameToTitle.append(i.split('\t', 1))

# Codigo HTML e regex para a criacao da nova coluna
collunm = "Login</th>\n<th>Users</th>"
collunmregex = r"Users</th>"

# Codigo HTML e regex para a criacao e preenchimento da tabela
login = "</a></td>\n<td><a>NOME-AQUI</a></td>"
loginregex = r"</a></td>\n"
loginNameRegex = r"NOME-AQUI"

# Regex para localizar os titulos
#regex = r"(?:\/)(\d{12})(?:\/)"

# Array que contem os titulos dos usuarios
#titulos = []

# Pegando arquivo user.html do squidanalyzer e adicionando a variavel html
arq = open('/var/www/squidanalyzer/2019/user.html', 'r')
html = arq.read()
arq.close()

# Aplicacao da regex para encontrar os titulos no codigo  HTML
#matches = re.finditer(regex, html, re.MULTILINE)
#i = 0

#for matchNum, match in enumerate(matches, start=1):
#
#  for groupNum in range(0, len(match.groups())):
#    groupNum = groupNum + 1#
     # Adicionando os titulos para o array de titulos
#    titulos.append(match.group(groupNum))
#    i += 1

# Verificando a necessidade de pos processamento
test_login_regex = r"Login</th>"
if (not re.search(test_login_regex, html)):

  # Localizando e substituindo o codigo HTML para a criacao da nova coluna na tabela
  html = re.sub(loginregex, login, html)
  html = re.sub(collunmregex, collunm, html)
  
  # Atualizando o arquivo de testes html.html
  arq = open('/var/www/html.html', 'w')
  arq.write(html)
  arq.close()
  
  # Abrindo arquivo html.html e separando as linhas
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
