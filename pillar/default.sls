#!py

def run():
    pillar = {
        'touchid': {
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
        pillar['touchid']['enabled'] = False

    return pillar