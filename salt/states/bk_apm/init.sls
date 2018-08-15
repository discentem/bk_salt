#!py

def run():
    config = {}

    role = __salt__['grains.get']('role', None)
    apm_packages = __salt__['pillar.get']("apm_packages:" + str(role), None)

    id = 'list apm_packages'
    config[id] = {
        'test.show_notification': [
          { 'text': apm_packages }
        ]
    }

    config["install apm packages"] = {
        'apm.packages_installed': [
            { 'packages': apm_packages }
        ]
    }

    return config
