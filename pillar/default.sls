#!py

def run():
    pillar = {
        'cpe_touchid': {
            'enabled': True,
        },
        'cpe_hosts': {
            'extra_entries': {
                # 'default': ['thing']
            }
        }
    }

    if __salt__['dates.today_is']('Friday'):
        pillar['cpe_hosts']['extra_entries'] = {
            'default' : ['thing']
        }
    if __grains__['os_family'] == 'Windows':
        pillar['cpe_touchid']['enabled'] = False

    return pillar