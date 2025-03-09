#!py

def run():

    run_list = [
        'states.sync_utils',
        'states.cpe_hosts',
        'states.cpe_touchid',
    ]

    return {
        'include': run_list
    }