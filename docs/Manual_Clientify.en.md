



# Clientify
  
Module to interact with Clientify.  

*Read this in other languages: [English](Manual_Clientify.md), [Português](Manual_Clientify.pr.md), [Español](Manual_Clientify.es.md)*
  
![banner](imgs/Banner_Clientify.png)
## How to install this module
  
To install the module in Rocketbot Studio, it can be done in two ways:
1. Manual: __Download__ the .zip file and unzip it in the modules folder. The folder name must be the same as the module and inside it must have the following files and folders: \__init__.py, package.json, docs, example and libs. If you have the application open, refresh your browser to be able to use the new module.
2. Automatic: When entering Rocketbot Studio on the right margin you will find the **Addons** section, select **Install Mods**, search for the desired module and press install.  


## Description of the commands

### Connects to Clientify
  
Connects to Clientify
|Parameters|Description|example|
| --- | --- | --- |
|Username|Clientify's username|username|
|Password|Clientify's password|********|
|Assign result to variable|Variable to assign the result. It will bring a JSON.|Variable|

### Get deals with filters
  
Gets all your deals with filters
|Parameters|Description|example|
| --- | --- | --- |
|Specific deals filter|Searching specific filter; e.g. deal's name, company name, contact name, contact last name, opportunity|Rocket|
|Owner's name|Owner's name filter|Charles|
|Filter greater than|Selector for greater than closed date||
|Closed date|Closed date greater than. Format yyyy/mm/dd|2021/08/23|
|Filter lesser than|Selector for lesser than closed date||
|Closed date|Closed date lesser than. Format yyyy/mm/dd|2021/08/23|
|Status|Deal's status. E.g. Won, Lost, Open, Expired.||
|Pipeline|Deal's pipeline filter.|Reseller|
|Date filter|Date's filter, created or modified.||
|Filter greater than|Selector for created date or modified date greater than.||
|Date|Created or modified date greater than. Format yyyy/mm/dd|2021/08/23|
|Filter lesser than|Selector for created date or modified date lesser than.||
|Date|Created or modified date lesser than. Format yyyy/mm/dd|2021/08/23|
|Assign result to variable|Variable to assign the result. It will bring a JSON.|Variable|

### Get deal by ID
  
Gets all propertys of a deal by ID
|Parameters|Description|example|
| --- | --- | --- |
|Deal ID|Deal ID. You can get it by list deals command or in the url in Clientify|2704232|
|Assign result to variable|Variable to assign the result. It will bring a JSON.|Variable|
|Only Deals information|If this box is checked, it will only bring the deal information.|True|

### Get products
  
This command allows you to get all products from Clientify
|Parameters|Description|example|
| --- | --- | --- |
|Assign result to variable|Variable to assign the result.|Variable|

### Get companies by query
  
This command allows you to get companies by name, after date of creation or after date of modification
|Parameters|Description|example|
| --- | --- | --- |
|Filter type|Filter type to apply. If you select Creation date or Modification date, it will bring all companies that have been created or modified after the selected date.||
|Value to search|Value to search in the filter.|Rocketbot|
|Assign result to variable|Variable to assign the result.|Variable|

### Get contacts by query
  
This command allows you to get contacts by name, phone or email.
|Parameters|Description|example|
| --- | --- | --- |
|Filter type|Filter type to apply.||
|Value to search|Value to search in the filter.|example@rocketbot.com|
|Assign result to variable|Variable to assign the result.|Variable|

### Create deal
  
This command allows you to create a deal.
|Parameters|Description|example|
| --- | --- | --- |
|Deal name|Name of the deal to create.|sell|
|Deal amount|Amount of the deal to create.|1500|
|Contact ID|ID of the contact to assign the deal.|39562459|
|Company ID|ID of the company to assign the deal.|39562459|
|Close date|Close date of the deal.|2023-03-20|
|Products|List of products of the deal.|[{"product_id":"4048412","quantity":1}, {"product_id":"4048413","quantity":2}]|
|Custom fields|List of custom fields of the deal.|[{"field": "field_name","value": "field_value"}, {"field": "field_name","value": "field_value"}]|
|Assign result to variable|Variable to assign the result.|Variable|
