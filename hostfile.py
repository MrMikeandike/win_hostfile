# script to view, add, and remove entries in windows host file
import os
import re

class hostfile:


    def __init__(self, fp=os.path.join(os.environ.get('windir'), 'system32', 'drivers', 'etc', 'hosts')):
        self.host_fp = fp

    def get(self, name=None, ip=None):
        with open(self.host_fp, 'r') as f:
            lines = [x.strip() for x in f.readlines() if bool(re.match(r"^\s*#", x)) is not True and x.strip() != '']

        entries = [{'ip':ip,'name':name} for ip,name in [re.split(r"\s+", line) for line in lines]]

        if name is not None:
            entries = [x for x in entries if x['name'] == name]
        if ip is not None:
            entries = [x for x in entries if x['ip'] == ip]

        return entries

    def add(self, name, ip):
        entries = self.get()
        entries.append({'ip': ip, 'name': name})

        entries_string = '\n'.join([f"{k} {v}" for k,v in [list(x.values()) for x in entries]])

        with open(self.host_fp, 'w') as f:
            f.write(entries_string)

    def remove(self, name, ip):
        entries = self.get()
        changelog = {'kept':[], 'removed':[]}

        for entry in entries:

            if entry['name'] == name and entry['ip'] == ip:
                changelog['removed'].append(entry)
            else:
                changelog['kept'].append(entry)

        with open(self.host_fp, 'w') as f:
            f.write('\n'.join([f"{k} {v}" for k,v in [list(x.values()) for x in changelog['kept']]]))
        print('REMOVED'.center(40, "-"))
        _ = [print(f"IP: {x['ip']};  NAME: {x['name']};") for x in changelog['removed']]
        return

# hf = hostfile()
# hf.add(ip='192.168.0.100', name='MyWebServer')
# hf.get()

#-- to remove

# hf.remove(ip='192.168.0.100', name='MyWebServer')
