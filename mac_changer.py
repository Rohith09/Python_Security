import subprocess
import optparse
import re


def get_argument():
    parser = optparse.OptionParser()
    parser.add_option("-i", "--interface", dest="interface", help="please specify your interface")
    parser.add_option("-m", "--mac", dest="new_mac", help="please specify your new mac address")

    (options, arguments) = parser.parse_args()

    if not options.interface:
        parser.error('-------> Please specify interface')
    elif not options.new_mac:
        parser.error('-------> Please specify new_mac')
    return options


def mac_change(interface, new_mac):
    print('change your interface ', interface, 'mac address to', new_mac)
    subprocess.call(['sudo', 'ifconfig', interface, 'down'])
    subprocess.call(['sudo', 'ifconfig', interface, 'hw', 'ether', new_mac])
    subprocess.call(['sudo', 'ifconfig', interface, 'up'])


options = get_argument()
mac_change(options.interface, options.new_mac)

mac_output = str(subprocess.check_output(['ifconfig', options.interface]))
mac_output_match = re.search(r'\w\w:\w\w:\w\w:\w\w:\w\w:\w\w', mac_output)

if mac_output_match:
    print('your mac address has been changed to', mac_output_match.group(0))
else:
    print('sorry, Mac changer fail')
