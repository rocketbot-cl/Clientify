import requests
import json

class ClientifyObject:

    def __init__(self, username, password):
        self.username = username
        self.password = password
        r = requests.post("https://api.clientify.net/v1/api-auth/obtain_token/", data={"username": self.username, "password": self.password})
        r = eval(r.content.decode())
        try:
            self.token = r["token"]
        except:
            self.token = ""

    def getDeals(self):
        headers = {"Authorization" : f"Token {self.token}", "Content-Type" : "application/json"}
        payload = ""
        r = requests.get("https://api.clientify.net/v1/deals", headers=headers, data=payload)
        r = json.loads(r.content.decode())
        return r

    def getDealsWithQuery(self, query, owner_name="", actual_closed_date={}, pipeline_desc=""):
        headers = {"Authorization" : f"Token {self.token}", "Content-Type" : "application/json"}
        payload = ""
        
        r = requests.get(f"https://api.clientify.net/v1/deals/?{query}", headers=headers, data=payload)
        r = r.json()
        
        contador = 2
        
        while r["next"] != None:
            r2 = requests.get(r["next"], headers=headers, data=payload)
            r2 = r2.json()
            
            for each in r2["results"]:
                r["results"].append(each)
           
            r["next"] = r2["next"]
            contador += 1

        if owner_name != "":
            a = {}

            a["results"] = [data for data in r["results"] if data["owner_name"] == owner_name]
            a["count"] = len(a["results"])
            r = a

        if actual_closed_date != "":
            a = {}

            if actual_closed_date["gt"] != False:

                a["results"] = [data for data in r["results"] if (data["actual_closed_date"]!= None) and (data["actual_closed_date"] > actual_closed_date["gt_date"])]
                a["count"] = len(a["results"])
                r = a
                a = {}
            if actual_closed_date["gte"] != False:

                a["results"] = [data for data in r["results"] if (data["actual_closed_date"]!= None) and (data["actual_closed_date"] >= actual_closed_date["gte_date"])]
                a["count"] = len(a["results"])
                r = a
                a = {}
            
            if actual_closed_date["lt"] != False:

                a["results"] = [data for data in r["results"] if (data["actual_closed_date"]!= None) and (data["actual_closed_date"] < actual_closed_date["lt_date"])]
                a["count"] = len(a["results"])
                r = a
                a = {}
            
            if actual_closed_date["lte"] != False:

                a["results"] = [data for data in r["results"] if (data["actual_closed_date"]!= None) and (data["actual_closed_date"] <= actual_closed_date["lte_date"])]
                a["count"] = len(a["results"])
                r = a
                a = {}
        
        if pipeline_desc != "":
            a = {}
            a["results"] = [data for data in r["results"] if (data["pipeline_desc"] == pipeline_desc)]
            a["count"] = len(a["results"])
            r = a
            a = {}
        
        return r
