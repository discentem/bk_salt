#!py

def run():
    return {
        "sync all": {
            "module.run": [
                {"name": "saltutil.sync_all"}, 
                {"kwargs": {"refresh": True}}
            ]
        }
    }