#!/usr/bin/python
import cgi
import requests
import sys
import commands

ERROR=False

#GRAB FORM INPUT
form = cgi.FieldStorage()
tgtip = form.getvalue('ip')

#GRAB SWITCHNAME
SWITCHNAME = commands.getstatusoutput('snmpwalk -v2c -c $SNMPKEY '+tgtip+' SNMPv2-MIB::sysName.0')
#CHECK FOR FUCKUP
if SWITCHNAME[1].startswith('Timeout:'): ERROR=True

#IF NOT FUCKED, GRAB INFO
if (ERROR == False):
	SWITCHNAME = SWITCHNAME[1].split('STRING: ')
	SWITCHNAME = SWITCHNAME[1]
	#GRAB INFO WITHOUT THE CRAP
	noflow = commands.getstatusoutput('snmpwalk -v2c -c $SNMPKEY '+tgtip+' 1.3.6.1.2.1.2.2.1.16 | grep ": 0"')
	noflow1 = noflow[1].split('\n')
	#STRIP OFF MORE CRAP
	lst = ([s.replace('IF-MIB::ifOutOctets', '') for s in noflow1])
	lst2 = ([s.replace(' = Counter32: 0', '') for s in lst])
	lst3 = ('a',)

	l = list(lst3)
	#GRAB INTERFACES BASED ON INDEXES THAT ARE 0
	for x in range(0,len(lst2)):
		y = commands.getstatusoutput('snmpwalk -v2c -c $SNMPKEY '+tgtip+' IF-MIB::ifName'+lst2[x])
		y = y[1].split('STRING: ')
		if y[1].startswith('Gi'):
			l.append(y[1])

	#REMOVE PORTS THAT SHOULD NOT BE REPORTED AGAINST (UNUSED UPLINKS)
	del l[0]
	if 'Gi1/1' in l: l.remove('Gi1/1')
        if 'Gi1/2' in l: l.remove('Gi1/2')	
	if 'Gi1/3' in l: l.remove('Gi1/3')
	if 'Gi1/4' in l: l.remove('Gi1/4')
	if 'Gi0/0' in l: l.remove('Gi0/0')
	if 'Gi1/1/1' in l: l.remove('Gi1/1/1')
	if 'Gi1/1/2' in l: l.remove('Gi1/1/2')
	if 'Gi2/1/1' in l: l.remove('Gi2/1/1')
	if 'Gi2/1/2' in l: l.remove('Gi2/1/2')
	if 'Gi3/1/1' in l: l.remove('Gi3/1/1')
	if 'Gi3/1/2' in l: l.remove('Gi3/1/2')
	if 'Gi4/1/1' in l: l.remove('Gi4/1/1')
	if 'Gi4/1/2' in l: l.remove('Gi4/1/2')
	if 'Gi5/1/1' in l: l.remove('Gi5/1/1')
	if 'Gi5/1/2' in l: l.remove('Gi5/1/2')
	if 'Gi6/1/1' in l: l.remove('Gi6/1/1')
	if 'Gi6/1/2' in l: l.remove('Gi6/1/2')

print "Content-type: text/html\n"
print "\n\n"
print "<HTML>"
print "<HEAD>"
print "<TITLE>Unused Ports Tool</TITLE>"
print "</HEAD>"
print "<CENTER>"
print "<BODY bgcolor='#3ead34'>"
#SCALE BASED ON SIZE OF RESULTS RETURNED
if (ERROR== False):
	print "<h1>There are "+str(len(l))+" unused port(s) on "+SWITCHNAME+" ("+tgtip+")</h1>"
	print "<TABLE bgcolor='#FFFFFF' border='1' cellpadding='15'><TR>"
	i=0
	scale = 3
	if len(l) > 9:	scale=6
	if len(l) > 49: scale=10
	if len(l) > 99: scale=12
	if len(l) > 149: scale=14
	for x in l:
		print "<td>"+x+"</td>"
		i+=1
		if i==scale:
			print "</tr><tr>"
			i=0
	print '</TABLE>'
else:
	print '<h1>Unable to connect to '+tgtip+'</h1>'
	print '<p>SNMP Response: '+SWITCHNAME[1]+'</p>'
print "<hr>"
print '<p>Check another switch</p>'
print '<h1>Switch IP:</h1>'
print '<form action="/ip/unusedports.py" method="post">'
print '<input autofocus title="Please enter the host IP appropriately!!" required type="text" name="ip">'
print '<input type="submit" value="Submit"><br>'
