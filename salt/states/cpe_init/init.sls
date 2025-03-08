#!py

def run():

    run_list = [
        'states.sync_utils',
        'states.cpe_hosts'
    ]

    return {
        'include': run_list
    }