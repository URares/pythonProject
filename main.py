import json
import requests
from bs4 import BeautifulSoup
import re
def checkIngredients(ingredients):
    for ing in ingredients:

        ing_name = ing.find(class_="wprm-recipe-ingredient-name").text

        if (ing.find(class_="wprm-recipe-ingredient-unit") is not None):
            try:

                json_ing[ing_name] = {'amount':  int(ing.find(class_="wprm-recipe-ingredient-amount").text) , 'unit': ing.find(class_="wprm-recipe-ingredient-unit").text}
            except ValueError:
                if('-' in ing.find(class_="wprm-recipe-ingredient-amount").text):
                    temp = ing.find(class_="wprm-recipe-ingredient-amount").text.split('-')[0]
                    json_ing[ing.find(class_="wprm-recipe-ingredient-name").text] = {
                        'amount': int(temp),
                        'unit': ing.find(class_="wprm-recipe-ingredient-unit").text}
                elif ('/' in ing.find(class_="wprm-recipe-ingredient-amount").text):
                    temp = ing.find(class_="wprm-recipe-ingredient-amount").text.split('/')[0]
                    json_ing[ing.find(class_="wprm-recipe-ingredient-name").text] = {
                        'amount': int(temp),
                        'unit': ing.find(class_="wprm-recipe-ingredient-unit").text}
                else:
                    json_ing[ing.find(class_="wprm-recipe-ingredient-name").text] = {
                     'amount': ing.find(class_="wprm-recipe-ingredient-amount").text,
                     'unit': ing.find(class_="wprm-recipe-ingredient-unit").text}

        elif(ing.find(class_="wprm-recipe-ingredient-amount") is not None) :
            try:
                json_ing[ing_name] = {'amount' : int(ing.find(class_="wprm-recipe-ingredient-amount").text) }
            except ValueError:
                json_ing[ing_name] = {'amount' : ing.find(class_="wprm-recipe-ingredient-amount").text }


def add_into_file(json_ing):
    try:
        fr = open("Cos de cumparaturi.txt", 'r')
        data = json.load(fr)

        for name,value in json_ing.items():
            if name in data.keys():
                print(name,data[name],value)
                for each_val in range(0,len(data[name])):
                    try:
                        all_units = [x['unit'] for x in data[name]]
                        if(value['unit'] not in all_units):
                            data[name].append(value)
                        elif data[name][each_val]['unit'] == value['unit'] and type(value['amount']) is int:
                            #print(name,data[name])
                            #print(value)
                            data[name][each_val]['amount'] += value['amount']
                        elif value['amount'] == 'putina':
                            data[name][each_val]['amount'] = 'multa'
                    except KeyError:
                        print(name,type(data[name][each_val]['amount']) , type(value['amount']))
                        if type(value['amount']) is int and type(data[name][each_val]['amount']) is int:
                            data[name][each_val]['amount'] += value['amount']
                        elif value['amount'] == 'putina' or value['amount'] == 'putina ':
                            data[name][each_val]['amount'] = 'multa'
                        elif type(value['amount'])is str and type(data[name][each_val]['amount']) is str:
                            data[name].append(value)

            else:
                data[name] = []
                data[name].append(value)
        with open("Cos de cumparaturi.txt",'w') as file:
           json.dump(data,file)

    except FileNotFoundError:
        fw = open("Cos de cumparaturi.txt",'w')
        for key in json_ing:
            i = []
            i.append(json_ing[key])
            json_ing[key]=i
        json.dump(json_ing,fw)



result = requests.get('https://jamilacuisine.ro/')
src = result.content
soup = BeautifulSoup(src,'html.parser')

tags = soup.find_all('a',href=re.compile("reteta-video"),class_="td-image-wrap")
for t in tags:
    reteta = t['href'].replace('https://jamilacuisine.ro/','')
    result = requests.get(f'https://jamilacuisine.ro/{reteta}')
    src = result.content
    soup = BeautifulSoup(src, 'html.parser')
    ingredients = soup.find_all("li", "wprm-recipe-ingredient")
    json_ing = {}
    checkIngredients(ingredients)
    add_into_file(json_ing)

fr = open("Cos de cumparaturi.txt")
jr = json.loads(fr.read())
print(json.dumps(jr,indent=3,sort_keys=True))