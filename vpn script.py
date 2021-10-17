import requests, os, sys, tempfile, subprocess, base64, time, random

def vpn_launch(country):

	country = country
	if len(country) == 2:
	    i = 6 
	elif len(country) > 2:
	    i = 5 
	else:
	    print('Country is too short!')
	    exit(1)

	try:
	    vpn_data = requests.get('http://www.vpngate.net/api/iphone/').text.replace('\r','')
	    servers = [line.split(',') for line in vpn_data.split('\n')]
	    labels = servers[1]
	    labels[0] = labels[0][1:]
	    servers = [s for s in servers[2:] if len(s) > 1]
	except:
	    print('Cannot get VPN servers data')
	    exit(1)

	desired = [s for s in servers if country.lower() in s[i].lower()]
	found = len(desired)
	print('Found ' + str(found) + ' servers for country ' + country)
	if found == 0:
	    exit(1)

	supported = [s for s in desired if len(s[-1]) > 0]
	print(str(len(supported)) + ' of these servers support OpenVPN')
	random_ip_int = random.randint(0,len(supported))-1
	# We pick the best servers by score
	winner = sorted(supported, key=lambda s: float(s[2].replace(',','.')), reverse=True)[random_ip_int]

	print("\n== Best server ==")
	pairs = list(zip(labels, winner))[:-1]
	for (l, d) in pairs[:4]:
	    print(l + ': ' + d)

	print(pairs[4][0] + ': ' + str(float(pairs[4][1]) / 10**6) + ' MBps')
	print("Country: " + pairs[5][1])

	print("\nLaunching VPN...")
	_, path = tempfile.mkstemp()
	f = open(path, 'w')
	f.write(base64.b64decode(winner[-1]).decode('utf-8'))
	f.write('\nscript-security 2\nup /etc/openvpn/update-resolv-conf\ndown /etc/openvpn/update-resolv-conf')
	f.close()

	x = subprocess.Popen(['sudo', 'openvpn', '--config', path])


def kill_vpn():
	print("KILLING VPN PROCESSES")
	os.system("sudo pkill openvpn")
	time.sleep(15)
	os.system("sudo killall -9 openvpn")
	time.sleep(15)
	print("******************")
	

def get_ip():
	ip = get('https://api.ipify.org').text
	return ip
my_ip = get_ip()
for i in range(5):
	vpn_launch("Korea")
	print("CONNECTING TO VPN")
	print("******************")
	time.sleep(20)
	ip = get_ip()
	if ip != my_ip:
		print("successfull")
		break

time.sleep(10000)
kill_vpn()
