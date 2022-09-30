from typing import List, Any, Dict
import json


class Scraper:
    def __init__(self, config: Any, client: Any):
        self.client = client
        self.config = config
    
    @staticmethod
    def _write_json(d: Dict, file: str):
        with open(file, "w") as fi:
            fi.write(json.dumps(d, indent=4))

    @staticmethod
    def _from_ids_to_name(client: Any, l_account: List):
        users = client.get_users(usernames=l_account)
        ids = [x.id for x in users.data]
        d = {}
        for id, name in zip(ids, l_account):
            d[name] = id
        return d

    def extract_ids_name(self):
        l_account = self.config.twitter_account[:10]
        client = self.client
        d = self._from_ids_to_name(
            client=client,
            l_account=l_account
        )
        self._write_json(d=d, file="name_ids.json")
        return 0
