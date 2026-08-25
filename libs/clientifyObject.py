"""Clientify client."""

__author__ = "Caleb Cipra"
__modified__ = "Danilo Toro, Nicolas Garcia"
__version__ = "2.0.0"
from tracemalloc import start

import requests
import json
import time

BASE_URL = "https://api-plus.clientify.com/v2"
global normalize_deal_value
def normalize_deal_value(value):
    if value is None:
        return "None"

    if isinstance(value, dict):
        return {
            key: normalize_deal_value(item)
            for key, item in value.items()
        }

    if isinstance(value, list):
        return [
            normalize_deal_value(item)
            for item in value
        ]

    return value

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
        r = requests.post(f"{BASE_URL}/api-auth/obtain_token/", data={"username": self.username, "password": self.password})
        r = eval(r.content.decode())
        try:
            self.token = r["token"]
        except:
            self.token = ""

    def getDeals(self)->list:
        """Get all deals."""
        headers = {"Authorization" : f"Token {self.token}", "Content-Type" : "application/json"}
        payload = ""
        r = requests.get(f"{BASE_URL}/deals", headers=headers, data=payload)
        r = json.loads(r.content.decode())
        return r

    def getDeal(self, deal_id:str, get_products=False)->dict:
        """Get deal."""
        get_products = (
            get_products is True
            or str(get_products).strip().lower() in ("true", "1", "yes")
        )

        headers = {"Authorization" : f"Token {self.token}", "Content-Type" : "application/json"}
        # payload = ""
        DEAL_BY_ID_FIELDS = ",".join([
            "url",
            "id",
            "owner",
            "owner_name",
            "owner_picture",
            "name",
            "amount",
            "amount_user",
            "currency",
            "contact",
            "contact_name",
            "contact_email",
            "contact_phone",
            "contact_medium",
            "contact_source",
            "created",
            "modified",
            "expected_closed_date",
            "actual_closed_date",
            "company",
            "company_name",
            "source",
            "deal_source",
            "status",
            "stages_duration",
            "status_desc",
            "probability",
            "probability_desc",
            "who_can_view",
            "pipeline_stage",
            "pipeline_stage_desc",
            "pipeline",
            "pipeline_desc",
            "involved_contacts",
            "tags",
            "remarks",
            "involved_companies",
            "wall_entries",
            "tasks",
            "events",
            "custom_fields",
            "products",
            "integrations",
            "lost_reason"
        ])
        # response = requests.get(f"{BASE_URL}/deals/{deal_id}", headers=headers, data=payload)
        #print(response.text)
        # result = response.json()
        response = requests.get(
            f"{BASE_URL}/deals/{deal_id}/",
            headers=headers,
            params={"fields": DEAL_BY_ID_FIELDS},
            timeout=60
        )

        if not response.ok:
            print(
                f"CLIENTIFY getDeal error ID {deal_id}: "
                f"status={response.status_code}"
            )
            print("CLIENTIFY response:", response.text[:2000])

        response.raise_for_status()
        result = response.json()

        if not isinstance(result, dict):
            raise ValueError(
                "Clientify returned an unexpected response for "
                f"deal {deal_id}: {repr(result)[:1000]}"
            )   
        
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
        STATUS_DESC_MAP = {
            "Ganada": "Won",
            "Perdida": "Lost",
            "Abierta": "Open"
        }
        result["status_desc"] = STATUS_DESC_MAP.get(
            result.get("status_desc"),
            result.get("status_desc")
        )

        result = normalize_deal_value(result)
        return result
    
    def getProducts(self, max_results:int=100):
        """Get deal products."""
        try:
            max_results = int(max_results)
        except (TypeError, ValueError):
            max_results = 100

        if max_results <= 0:
            max_results = 100

        headers = {"Authorization" : f"Token {self.token}", "Content-Type" : "application/json"}
        # payload = ""
        PRODUCT_FIELDS = ",".join([
            "id",
            "name",
            "description",
            "created",
            "price",
            "currency",
            "currency_format",
            "owner",
            "sku",
            "modified",
            "categories",
            "sub_categories",
            "product_picture_url",
            "term_length",
            "source",
            "payment",
            "payment_period",
            "custom_fields",
            "all_categories",
            "all_subcategories",
            "logo",
            "picture_url",
            "owner_name",
            "product_url_external",
            "product_url",
            "tax"
        ])
        # r = requests.get(f"{BASE_URL}/products/", headers=headers, data=payload)
        # r = r.json()
        # return r["results"]
        response = requests.get(
            f"{BASE_URL}/products/",
            headers=headers,
            params={"fields": PRODUCT_FIELDS},
            timeout=60
        )

        if not response.ok:
            print(
                "CLIENTIFY getProducts error:",
                response.status_code,
                response.text[:2000]
            )

        response.raise_for_status()
        result = response.json()

        if not isinstance(result, dict):
            raise ValueError(
                "Clientify returned an unexpected response in getProducts: "
                f"{repr(result)[:1000]}"
            )

        products = result.get("results")

        if not isinstance(products, list):
            raise ValueError(
                "Clientify did not return a valid product list: "
                f"{repr(result)[:1000]}"
            )
        
        # Si la primera página ya supera el límite
        products = products[:max_results]
        next_url = result.get("next")
        visited_urls = set()

        while next_url and len(products) < max_results:
            # Evita un bucle infinito si la API repite la misma página
            if next_url in visited_urls:
                raise ValueError(
                    "Clientify repeated the same pagination URL "
                    f"in getProducts: {next_url}"
                )

            visited_urls.add(next_url)

            next_response = requests.get(
                next_url,
                headers=headers,
                timeout=60
            )

            if not next_response.ok:
                print(
                    "CLIENTIFY getProducts pagination error:",
                    next_response.status_code,
                    next_response.text[:2000]
                )

            next_response.raise_for_status()
            next_result = next_response.json()

            if not isinstance(next_result, dict):
                raise ValueError(
                    "Clientify returned an unexpected paginated response "
                    f"in getProducts: {repr(next_result)[:1000]}"
                )

            next_products = next_result.get("results")

            if not isinstance(next_products, list):
                raise ValueError(
                    "Clientify did not return a valid product list "
                    f"in a paginated response: {repr(next_result)[:1000]}"
                )
            remaining = max_results - len(products)
            products.extend(next_products[:remaining])
            next_url = next_result.get("next")

        return normalize_deal_value(products)

    def getDealsWithQuery(self, query:str, owner_name:str="", actual_closed_date:dict = None, pipeline_desc: str = ""
    ) -> list:
        """Get deals with query."""

        actual_closed_date = actual_closed_date or {}
        headers = {"Authorization" : f"Token {self.token}", "Content-Type" : "application/json"}

        DEAL_FIELDS = ",".join([
            "url",
            "id",
            "owner_name",
            "name",
            "contact",
            "contact_name",
            "contact_email",
            "contact_phone",
            "contact_medium",
            "contact_source",
            "company",
            "company_name",
            "amount",
            "amount_user",
            "currency",
            "status",
            "status_desc",
            "probability",
            "probability_desc",
            "pipeline_stage",
            "pipeline",
            "pipeline_desc",
            "pipeline_stage_desc",
            "tags",
            "custom_fields",
            "created",
            "modified",
            "expected_closed_date",
            "actual_closed_date",
            "deal_source"
        ])
        FILTER_FIELDS = ",".join([
            "id",
            "owner_name",
            "actual_closed_date",
            "pipeline_desc"
        ])
        page = 1
        start = time.time()
        params = {
            "fields": FILTER_FIELDS
        }

        if actual_closed_date:
            if actual_closed_date.get("gt"):
                params["actual_closed_date[gt]"] = actual_closed_date["gt_date"]

            if actual_closed_date.get("gte"):
                params["actual_closed_date[gte]"] = actual_closed_date["gte_date"]

            if actual_closed_date.get("lt"):
                params["actual_closed_date[lt]"] = actual_closed_date["lt_date"]

            if actual_closed_date.get("lte"):
                params["actual_closed_date[lte]"] = actual_closed_date["lte_date"]

        response = requests.get(
            f"{BASE_URL}/deals/?{query}",
            headers=headers,
            params=params,
            timeout=60
        )

        response.raise_for_status()
        r = response.json()


        if isinstance(r, list):
            r = {
                "count": len(r),
                "next": None,
                "results": r
            }
        elif not isinstance(r, dict):
            raise ValueError(
                f"Unexpected Clientify format: {type(r).__name__}"
            )

        if not isinstance(r.get("results"), list):
            raise ValueError(
                "Clientify did not return 'results' as a list. "
                f"Response: {repr(r)[:1000]}"
            )

        invalid_items = [
            item for item in r["results"]
            if not isinstance(item, dict)
        ]

        if invalid_items:
            raise ValueError(
                "Clientify returned items that are not deals. "
                f"First item: {repr(invalid_items[0])[:500]}"
            )
        
    
        while r.get("next"):
            page += 1
            response2 = requests.get(
                r["next"],
                headers=headers,
                timeout=60
            )
            response2.raise_for_status()
            r2 = response2.json()

            if not isinstance(r2.get("results"), list):
                raise ValueError(
                    "Clientify returned a page without valid 'results'. "
                    f"Response: {repr(r2)[:1000]}"
                )

            r["results"].extend(r2["results"])
            r["next"] = r2.get("next")

        results = r.get("results", [])

        if owner_name:
            results = [
                deal for deal in results
                if deal.get("owner_name") == owner_name
            ]

        if pipeline_desc:
            results = [
                deal for deal in results
                if deal.get("pipeline_desc") == pipeline_desc
            ]

        if actual_closed_date:
            if actual_closed_date.get("gt"):
                results = [
                    deal for deal in results
                    if deal.get("actual_closed_date")
                    and deal["actual_closed_date"] > actual_closed_date["gt_date"]
                ]

            if actual_closed_date.get("gte"):
                results = [
                    deal for deal in results
                    if deal.get("actual_closed_date")
                    and deal["actual_closed_date"] >= actual_closed_date["gte_date"]
                ]

            if actual_closed_date.get("lt"):
                results = [
                    deal for deal in results
                    if deal.get("actual_closed_date")
                    and deal["actual_closed_date"] < actual_closed_date["lt_date"]
                ]

            if actual_closed_date.get("lte"):
                results = [
                    deal for deal in results
                    if deal.get("actual_closed_date")
                    and deal["actual_closed_date"] <= actual_closed_date["lte_date"]
                ]

        r["results"] = results
        r["count"] = len(results)
        r["next"] = None

        # Obtener el detalle completo solamente de los negocios coincidentes
        detailed_results = []

        for index, deal in enumerate(results, start=1):
            deal_id = deal["id"]

            detail_response = requests.get(
                f"{BASE_URL}/deals/{deal_id}",
                headers=headers,
                params={"fields": DEAL_FIELDS},
                timeout=60
            )

            if not detail_response.ok:
                print(
                    f"CLIENTIFY deal detail error ID {deal_id}: "
                    f"status={detail_response.status_code}"
                )
                print("CLIENTIFY error response:", detail_response.text[:2000])

            detail_response.raise_for_status()
            detail = detail_response.json()

            if not isinstance(detail, dict):
                raise ValueError(
                    f"Clientify returned invalid detail for deal {deal_id}: "
                    f"{repr(detail)[:500]}"
                )

            detailed_results.append(detail)


        STATUS_DESC_MAP = {
            "Ganada": "Won"
        }

        r["total_amount"] = sum(
            float(deal.get("amount") or 0)
            for deal in detailed_results
        )
        for deal in detailed_results:
            if "status_desc" in deal:
                deal["status_desc"] = STATUS_DESC_MAP.get(
                    deal["status_desc"],
                    deal["status_desc"]
                )

            for key, value in deal.items():
                deal[key] = normalize_deal_value(value)

        r["results"] = detailed_results
        r["count"] = len(detailed_results)
        r["next"] = None
        return r
    
    
    def createDeal(self, data):
        """Create deal."""
        if not isinstance(data, dict):
            raise ValueError(
                "createDeal data must be a dictionary."
            )

        required_fields = {
            "name": data.get("name"),
            "amount": data.get("amount"),
            "contact": data.get("contact"),
            "company": data.get("company"),
            "expected_closed_date": data.get(
                "expected_closed_date"
            )
        }

        missing_fields = [
            field_name
            for field_name, field_value in required_fields.items()
            if field_value in (None, "")
        ]

        if missing_fields:
            raise ValueError(
                "Missing required createDeal fields: "
                + ", ".join(missing_fields)
            )

        try:
            float(data["amount"])
        except (TypeError, ValueError):
            raise ValueError(
                "Deal amount must be numeric. "
                f"Received: {repr(data.get('amount'))}"
            )
        headers = {"Authorization" : f"Token {self.token}", "Content-Type" : "application/json"}
        r = requests.post(f"{BASE_URL}/deals/", headers=headers, json=data)
        if not r.ok:
            print(
                "CLIENTIFY createDeal error:",
                r.status_code,
                r.text[:4000]
            )

        r.raise_for_status()

        try:
            result = r.json()
        except ValueError:
            raise ValueError(
                "Clientify created or processed the deal but returned "
                "a non-JSON response: "
                f"{r.text[:2000]}"
            )

        if not isinstance(result, dict):
            raise ValueError(
                "Clientify returned an unexpected createDeal response: "
                f"{repr(result)[:2000]}"
            )

        return result
        
    def getCustomFields(self):
        """Get custom fields."""
        headers = {"Authorization" : f"Token {self.token}", "Content-Type" : "application/json"}
        payload = ""
        r = requests.get(f"{BASE_URL}/custom-fields", headers=headers, data=payload)
        r = r.json()
        return r
    
    def dealPipelineStages(self):
        """Get deal pipeline stages."""
        headers = {"Authorization" : f"Token {self.token}", "Content-Type" : "application/json"}
        data = {
            "content_type": "deal"
        }
        payload = json.dumps(data)
        r = requests.get(f"{BASE_URL}/deals/pipelines/stages", headers=headers, data=payload)
        r = r.json()
        return r

    def getCompanies(self, filter_type, filter_value, max_results=100):
        """Get companies."""
        try:
            max_results = int(max_results)
        except (TypeError, ValueError):
            max_results = 100

        if max_results <= 0:
            max_results = 100

        headers = {"Authorization" : f"Token {self.token}", "Content-Type" : "application/json"}
        COMPANY_FIELDS = ",".join([
            "url",
            "id",
            "name",
            "company_sector",
            "number_of_employees",
            "number_of_employees_desc",
            "owner",
            "owner_name",
            "custom_fields",
            "picture_url",
            "facebook_url",
            "linkedin_url",
            "twitter_url",
            "last_viewed",
            "last_interaction",
            "created",
            "modified",
            "taxpayer_identification_number"
        ])

        params = {
            "fields": COMPANY_FIELDS
        }

        if filter_type and filter_value:
            params[filter_type] = filter_value

        r = requests.get(
            f"{BASE_URL}/companies/",
            headers=headers,
            params=params,
            timeout=60
        )
        if not r.ok:
            print(
                "CLIENTIFY getCompanies error:",
                r.status_code,
                r.text[:2000]
            )
        r.raise_for_status()

        r = r.json()
        # return r["results"]
        if not isinstance(r, dict):
            raise ValueError(
                "Clientify returned an unexpected response: "
                f"{repr(r)[:1000]}"
            )
        
        results = r.get("results")
        if not isinstance(results, list):
            raise ValueError(
                "Clientify did not return a valid company list: "
                f"{repr(r)[:1000]}"
            )
        # Respeta el límite incluso si la primera página trae más resultados.
        results = results[:max_results]

        next_url = r.get("next")
        visited_urls = set()

        while next_url and len(results) < max_results:
            # Evita un bucle infinito si Clientify repite la misma URL.
            if next_url in visited_urls:
                raise ValueError(
                    "Clientify repeated the same pagination URL "
                    f"in getCompanies: {next_url}"
                )

            visited_urls.add(next_url)

            next_response = requests.get(
                next_url,
                headers=headers,
                timeout=60
            )

            if not next_response.ok:
                print(
                    "CLIENTIFY getCompanies pagination error:",
                    next_response.status_code,
                    next_response.text[:2000]
                )

            next_response.raise_for_status()
            next_result = next_response.json()

            if not isinstance(next_result, dict):
                raise ValueError(
                    "Clientify returned an unexpected paginated response "
                    f"in getCompanies: {repr(next_result)[:1000]}"
                )

            next_companies = next_result.get("results")

            if not isinstance(next_companies, list):
                raise ValueError(
                    "Clientify did not return a valid company list "
                    f"in a paginated response: {repr(next_result)[:1000]}"
                )

            remaining = max_results - len(results)
            results.extend(next_companies[:remaining])

            next_url = next_result.get("next")

        return normalize_deal_value(results)
    
    def getContacts(self, filter_type, filter_value, max_results=100):
        """Get contacts with an optional filter."""
        headers = {"Authorization" : f"Token {self.token}", "Content-Type" : "application/json"}
        try:
            max_results = int(max_results)
        except (TypeError, ValueError):
            max_results = 100

        if max_results <= 0:
            max_results = 100

        CONTACT_FIELDS = ",".join([
            "id",
            "owner_id",
            "first_name",
            "last_name",
            "status",
            "title",
            "company_id",
            "contact_type",
            "contact_source",
            "picture_url",
            "description",
            "remarks",
            "summary",
            "created",
            "owner_name",
            "owner",
            "company_name",
            "taxpayer_identification_number",
            "medium",
            "channel",
            "emails",
            "phones",
            "addresses",
            "custom_fields",
            "tags",
            "modified",
            "last_contact",
            "birthday",
            "gdpr_accept",
            "gdpr_acceptance_date",
            "disclaimer"
        ])
        params = {"fields": CONTACT_FIELDS}

        # if filter_type and filter_value not in (None, ""):
        #     params[filter_type] = filter_value

        filter_type = str(filter_type or "").strip().lower()
        filter_value = (
            str(filter_value).strip()
            if filter_value not in (None, "")
            else ""
        )

        filter_type = str(filter_type or "").strip().lower()

        filter_value = (
            str(filter_value).strip()
            if filter_value not in (None, "")
            else ""
        )

        valid_filters = {
            "all",
            "todos",
            "name",
            "nombre",
            "query",
            "phone",
            "telefono",
            "teléfono",
            "email"
        }

        if filter_type not in valid_filters and filter_type != "":
            raise ValueError(
                "Invalid contact filter. Valid values are: "
                "all, name, phone, email."
            )

        # La API v2 utiliza query para buscar por nombre, correo electrónico o teléfono.
        if filter_type not in ("", "all", "todos"):
            if not filter_value:
                raise ValueError(
                    f"A value is required for filter '{filter_type}'."
                )

            params["query"] = filter_value

        print(
            "CLIENTIFY getContacts request:",
            f"{BASE_URL}/contacts/",
            params
        )

        response = requests.get(
            f"{BASE_URL}/contacts/",
            headers=headers,
            params=params,
            timeout=60
        )

        if not response.ok:
            print(
                "CLIENTIFY getContacts error:",
                response.status_code,
                response.text[:2000]
            )

        response.raise_for_status()
        result = response.json()

        if isinstance(result, dict):
            contacts = result.get("results")

            if not isinstance(contacts, list):
                raise ValueError(
                    "Clientify did not return a valid contact list: "
                    f"{repr(result)[:1000]}"
                )

            next_url = result.get("next")

        # Lo mantenemos por compatibilidad si alguna ruta devuelve lista directa.
        elif isinstance(result, list):
            contacts = result
            next_url = None

        else:
            raise ValueError(
                "Clientify returned an unexpected response "
                f"in getContacts: {repr(result)[:1000]}"
            )

        contacts = contacts[:max_results]
        visited_urls = set()

        while next_url and len(contacts) < max_results:
            if next_url in visited_urls:
                raise ValueError(
                    "Clientify repeated the same pagination URL "
                    f"in getContacts: {next_url}"
                )

            visited_urls.add(next_url)

            next_response = requests.get(
                next_url,
                headers=headers,
                timeout=60
            )

            if not next_response.ok:
                print(
                    "CLIENTIFY getContacts pagination error:",
                    next_response.status_code,
                    next_response.text[:2000]
                )

            next_response.raise_for_status()
            next_result = next_response.json()

            if not isinstance(next_result, dict):
                raise ValueError(
                    "Clientify returned an unexpected paginated response "
                    f"in getContacts: {repr(next_result)[:1000]}"
                )

            next_contacts = next_result.get("results")

            if not isinstance(next_contacts, list):
                raise ValueError(
                    "Clientify did not return a valid contact list "
                    f"in a paginated response: {repr(next_result)[:1000]}"
                )

            remaining = max_results - len(contacts)
            contacts.extend(next_contacts[:remaining])
            next_url = next_result.get("next")

        return normalize_deal_value(contacts)

    

if __name__ == "__main__":
    pass