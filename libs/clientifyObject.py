"""Clientify client."""

__author__ = "Caleb Cipra"
__modified__ = "Danilo Toro, Nicolas Garcia"
__version__ = "2.0.0"
import requests
import json

class ClientifyObject:
    """Clientify client.

    Attributes:
        username (str): Clientify username.
        password (str): Clientify password.
        token (str): Clientify token.
    
    Methods:
        getDeals()
        getDeal(deal_id)
        getDealsWithQuery(query, owner_name="", actual_closed_date={}, pipeline_desc="")
    """

    def __init__(self, username:str, password:str):
        """Initialize Clientify client."""
        self.username = username
        self.password = password
        r = requests.post("https://api.clientify.net/v1/api-auth/obtain_token/", data={"username": self.username, "password": self.password})
        r = eval(r.content.decode())
        try:
            self.token = r["token"]
        except:
            self.token = ""

    def getDeals(self)->list:
        """Get all deals."""
        headers = {"Authorization" : f"Token {self.token}", "Content-Type" : "application/json"}
        payload = ""
        r = requests.get("https://api.clientify.net/v1/deals", headers=headers, data=payload)
        r = json.loads(r.content.decode())
        return r

    def getDeal(self, deal_id:str, get_products=False)->dict:
        """Get deal."""
        headers = {"Authorization" : f"Token {self.token}", "Content-Type" : "application/json"}
        payload = ""
        response = requests.get(f"https://api.clientify.net/v1/deals/{deal_id}", headers=headers, data=payload)
        #print(response.text)
        result = response.json()
                    
        if get_products: 
            tmp_products = result["products"] #este devuelve cantidad (GetDeal nativo)
            # result2 Retorna de GetProducts los que tengan el mismo ID (pero no tiene cantidad)
            result2= list(filter(lambda x: x["id"] in [product["product_id"] for product in result["products"]],self.getProducts()))
            # Creando un diccionario para mapear IDs y cantidades de result para agregar en result 2
            cantidades_por_id = {producto["product_id"]: producto["quantity"] for producto in result["products"]}
            for producto in result2:
                producto["quantity"] = cantidades_por_id[producto["id"]]

            result["products"] = result2
            if len(result2) == 0:
                result["products"] = tmp_products
            
        return result
    

    def getProducts(self):
        """Get deal products."""
        headers = {"Authorization" : f"Token {self.token}", "Content-Type" : "application/json"}
        payload = ""
        r = requests.get(f"https://api.clientify.net/v1/products/", headers=headers, data=payload)
        r = r.json()
        return r["results"]
        


    def getDealsWithQuery(self, query:str, owner_name:str="", actual_closed_date:dict={}, pipeline_desc:str="")->list:
        """Get deals with query."""
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
    
    
    def createDeal(self, data):
        """Create deal."""
        headers = {"Authorization" : f"Token {self.token}", "Content-Type" : "application/json"}
        payload = json.dumps(data)
        r = requests.post("https://api.clientify.net/v1/deals/", headers=headers, data=payload)
        r = r.json()
        return r
        
    def getCustomFields(self):
        """Get custom fields."""
        headers = {"Authorization" : f"Token {self.token}", "Content-Type" : "application/json"}
        payload = ""
        r = requests.get(f"https://api.clientify.net/v1/custom-fields", headers=headers, data=payload)
        r = r.json()
        return r
    
    def dealPipelineStages(self):
        """Get deal pipeline stages."""
        headers = {"Authorization" : f"Token {self.token}", "Content-Type" : "application/json"}
        data = {
            "content_type": "deal"
        }
        payload = json.dumps(data)
        r = requests.get("https://api.clientify.net/v1/deals/pipelines/stages", headers=headers, data=payload)
        r = r.json()
        return r

    def getCompanies(self, filter_type, filter_value):
        """Get companies."""
        headers = {"Authorization" : f"Token {self.token}", "Content-Type" : "application/json"}
        payload = ""
        url = f"https://api.clientify.net/v1/companies/?{filter_type}={filter_value}"
        r = requests.get(url, headers=headers, data=payload)
        r = r.json()
        return r["results"]
    
    def getContacts(self, filter_type, filter_value):
        """Get contacts."""
        headers = {"Authorization" : f"Token {self.token}", "Content-Type" : "application/json"}
        payload = ""
        r = requests.get(f"https://api.clientify.net/v1/contacts/?{filter_type}={filter_value}", headers=headers, data=payload)
        r = r.json()
        return r["results"]
    

if __name__ == "__main__":
    pass