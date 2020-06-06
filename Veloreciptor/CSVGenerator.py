import json
import pandas as pd

recipes = pd.DataFrame(columns=['id', 'url', 'title', 'portions', 'category', 'preparation'])
ingredients = pd.DataFrame(columns=['id', 'name'])
fact_table = pd.DataFrame(columns=['recipe_id', 'product_id', 'amount', 'measure'])

with open("recipes.json", encoding='utf-8') as f:
    data = json.load(f)

for recipe in data:
    recipe_id = recipes.shape[0]
    recipe_input = input("{1}\nIngredient length is {0}. Leave empty to continue.".format(
            len(recipe['ingredients']), recipe['title']))
    if recipe_input == 'quit':
        break
    elif recipe_input:
        continue
    preparation = [i.replace("\r\n", " ").replace("\n", " ") for i in recipe['preparation']]
    recipes = recipes.append(
        {"id": recipe_id, "url": recipe['link'], "title": recipe['title'], "preparation": preparation,
         "portions": recipe['portions'], "category": recipe['category']},
        ignore_index=True
    )
    for ingredient in recipe['ingredients']:
        print(ingredient)
        name = input("Name: ")
        if not name:
            continue
        quantity = input("Quantity: ")
        measure = input("Measure: ")
        ingredient_id = None
        row = ingredients.loc[ingredients['name'] == name]
        if row.empty:
            ingredient_id = ingredients.shape[0]
            ingredients = ingredients.append(
                {'id': ingredient_id, 'name': name},
                ignore_index=True
            )
        else:
            ingredient_id = row.iloc[0]['id']
        fact_table = fact_table.append(
            {'recipe_id': recipe_id, 'product_id': ingredient_id, 'amount': quantity, 'measure': measure},
            ignore_index=True
        )
