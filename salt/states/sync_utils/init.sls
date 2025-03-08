#!py

def run():
    return {
        "sync_utilities": {
            "module.run": [
                {"name": "saltutil.sync_modules"}, 
                {"kwargs": {"refresh": True}}
            ]
        }
    }