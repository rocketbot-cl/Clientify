# coding: utf-8
"""
Base para desarrollo de modulos externos.
Para obtener el modulo/Funcion que se esta llamando:
     GetParams("module")

Para obtener las variables enviadas desde formulario/comando Rocketbot:
    var = GetParams(variable)
    Las "variable" se define en forms del archivo package.json

Para modificar la variable de Rocketbot:
    SetVar(Variable_Rocketbot, "dato")

Para obtener una variable de Rocketbot:
    var = GetVar(Variable_Rocketbot)

Para obtener la Opcion seleccionada:
    opcion = GetParams("option")


Para instalar librerias se debe ingresar por terminal a la carpeta "libs"
    
    pip install <package> -t .

"""



import os
import sys

__author__ = "Caleb Cipra"
__modified__ = "Danilo Toro"
__version__ = "1.1.0"


GetParams = GetParams #type:ignore
SetVar = SetVar #type:ignore
base_path = tmp_global_obj["basepath"] #type:ignore


cur_path = base_path + 'modules' + os.sep + 'Clientify' + os.sep + 'libs' + os.sep
if cur_path not in sys.path:
    sys.path.append(cur_path)

from clientifyObject import ClientifyObject #type:ignore

global clientify_I

module = GetParams("module")

try:

    if module == "connectToClientify":

        username = GetParams("username")
        password = GetParams("password")
        
        clientify_I = ClientifyObject(username, password)

        resultConnection = False

        if clientify_I.token != "":
            resultConnection = True
        
        whereToStore = GetParams("whereToStore")
        SetVar(whereToStore, resultConnection)
    
    if (module == "getDealsWithQuery"):
        
        deals_filter = GetParams("deals_filter")
        if deals_filter:
            deals_filter = "query=" + deals_filter
        else:
            deals_filter = ""
        
        status_id = GetParams("status_id")
        if status_id:
            status_id = "status_id=" + status_id
        else:
            status_id = ""

        date_filter = GetParams("date_filter")
        date_filter_1 = ""
        date_filter_2 = ""
        
        if date_filter:
            greater_filter = GetParams("greater_filter")
            if greater_filter:   
                date_greater = GetParams("date_greater")
                date_filter_1 += f"{date_filter}{greater_filter}={date_greater}"
            lesser_filter = GetParams("lesser_filter")
            if lesser_filter:
                date_lesser = GetParams("date_lesser")
                date_filter_2 += f"{date_filter}{lesser_filter}={date_lesser}"
        
        owner_name = GetParams("owner_name")
        if not owner_name:
            owner_name = ""

        query = f"{deals_filter}&{status_id}&{date_filter_1}&{date_filter_2}"

        closed_date_greater_filter = GetParams("closed_date_greater_filter")
        closed_date_greater = GetParams("closed_date_greater")
        closed_date_lesser_filter = GetParams("closed_date_lesser_filter")
        closed_date_lesser = GetParams("closed_date_lesser")
        
        actual_closed_date = {"gt" : False, "gte" : False, "lt" : False, "lte" : False, "gt_date" : "", "gte_date" : "", "lt_date" : "", "lte_date" : ""}
        
        if closed_date_greater_filter:
            closed_date_greater = closed_date_greater.replace("/", "-")
            actual_closed_date[closed_date_greater_filter] = True
            actual_closed_date[f"{closed_date_greater_filter}_date"] = closed_date_greater
        if closed_date_lesser_filter:
            closed_date_lesser = closed_date_lesser.replace("/", "-")
            actual_closed_date[closed_date_lesser_filter] = True
            actual_closed_date[f"{closed_date_lesser_filter}_date"] = closed_date_lesser

        pipeline_desc = GetParams("pipeline_desc")
        if not pipeline_desc:
            pipeline_desc = ""

        resultRead = clientify_I.getDealsWithQuery(query, owner_name, actual_closed_date, pipeline_desc)

        whereToStore = GetParams("whereToStore")
        SetVar(whereToStore, resultRead)

    if module == "getDeal":
        deal_id = GetParams("deal_id")
        resultRead = clientify_I.getDeal(deal_id, True)
        whereToStore = GetParams("whereToStore")
        SetVar(whereToStore, resultRead)

except Exception as e:
    print("\x1B[" + "31;40mAn error occurred\x1B[" + "0m")
    PrintException() #type:ignore
    raise e
