import requests
import json
import time
import pandas as pd
import warnings
warnings.simplefilter('ignore', FutureWarning)
import random

# recipe_apikey = '1088202091947710174'
# food = "鮭"
def get_recipe(recipe_apikey, food):
    
    URL = 'https://app.rakuten.co.jp/services/api/Recipe/CategoryList/20170426?applicationId=' + recipe_apikey
    res = requests.get(URL)
    recipe_url = []
    json_data = json.loads(res.text)
    
    parent_dict = {} 
    df = pd.DataFrame(columns=['category1','category2','category3','categoryId','categoryName'])
    
    for category in json_data['result']['large']:
        df = df.append({'category1':category['categoryId'],'category2':"",'category3':"",
                        'categoryId':category['categoryId'],'categoryName':category['categoryName']}, 
                        ignore_index=True)
        
    for category in json_data['result']['medium']:
        df = df.append({'category1':category['parentCategoryId'],'category2':category['categoryId'],
                        'category3':"",'categoryId':str(category['parentCategoryId'])+"-"+str(category['categoryId']),
                        'categoryName':category['categoryName']}, ignore_index=True)
        parent_dict[str(category['categoryId'])] = category['parentCategoryId']
        
    for category in json_data['result']['small']:
        df = df.append({'category1':parent_dict[category['parentCategoryId']],'category2':category['parentCategoryId'],
                        'category3':category['categoryId'],'categoryId':parent_dict[category['parentCategoryId']]+"-"+str(category['parentCategoryId'])+"-"+str(category['categoryId']),
                        'categoryName':category['categoryName']}, ignore_index=True)
        
    df_keyword = df[df["categoryName"].str.contains(food)]
    notemp = df_keyword.empty
    if notemp != False:
        df_recipe = None
        return notemp, df_recipe
    else:
        df_keyword = df_keyword['categoryId'].to_list()
        df_recipe = pd.DataFrame(columns=['recipeId', 'recipeTitle', 'foodImageUrl', 'recipeMaterial', 'recipeCost', 'recipeIndication', 'categoryId', 'categoryName'])
        URL2 = 'https://app.rakuten.co.jp/services/api/Recipe/CategoryRanking/20170426?applicationId=' + recipe_apikey + '&categoryId='
        
        for i in range(2):
            time.sleep(1) 
            randint = random.randrange(len(df_keyword))
            row = df_keyword[randint]
            url = URL2 + row
            res = requests.get(url)
            
            json_data = json.loads(res.text)
            recipes = json_data['result']
            
            for recipe in recipes:
                _url = 'https://recipe.rakuten.co.jp/recipe/' + str(recipe['recipeId'])
                recipe_url.append(_url)
                df_recipe = df_recipe.append({'recipeTitle':recipe['recipeTitle'],'foodImageUrl':recipe['foodImageUrl'],'recipeMaterial':recipe['recipeMaterial'],
                                            'recipeCost':recipe['recipeCost'],'recipeIndication':recipe['recipeIndication'],}, ignore_index=True)
        df_recipe = df_recipe.drop(['categoryId','categoryName',], axis=1)
        return notemp, df_recipe, recipe_url

# df_recipe = get_recipe(recipe_apikey, food)

# print(df_recipe['recipeTitle'].to_list())
# print(df_recipe['foodImageUrl'].to_list())
# print(df_recipe['recipeMaterial'].to_list())
# print(df_recipe['recipeCost'].to_list())
# print(df_recipe['recipeIndication'].to_list())
