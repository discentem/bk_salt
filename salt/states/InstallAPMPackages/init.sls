#!py

def run():
    config = {}

    role = __salt__['grains.get']('role', None)
    apm_packages = __salt__['pillar.get']("apm_packages:" + str(role), None)

    for package in apm_packages:

        unless_value = 'if ([boolean](apm list | select-string %s)) { exit 0 } else { exit 1 }' % package

        config['install apm package: {0}'.format(package)] = {
            'cmd.run': [
                { 'name': 'apm install {0}'.format(package) },
                { 'shell': "powershell" },
                { 'unless': unless_value }
            ]
        }

    return config
