#!py

def run():
    config = {}

    apm_packages = __salt__['pillar.get']("apm_packages", None)

    if apm_packages != None:
        config["install apm packages"] = {
            'apm.installed': [
                { 'packages': apm_packages },
                { 'apm_cmd': "C:\Program Files\Atom Beta\\resources\cli\\apm.cmd" },
                { 'hard': True }
            ]
        }
        # config['uninstall apm packages'] = {
        #     'apm.uninstalled': [
        #         { 'packages': apm_packages },
        #         { 'apm_cmd': "C:\Program Files\Atom Beta\\resources\cli\\apm.cmd" }
        #     ]
        # }

    return config
