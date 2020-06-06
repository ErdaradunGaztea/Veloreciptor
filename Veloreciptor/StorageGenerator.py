import pandas as pd
import numpy as np

recipes = pd.read_csv('data/KK_recipes.csv').set_index('id')
products = pd.read_csv('data/products.csv').set_index('id')
rec_ingr = pd.read_csv('data/KK_recipe_ingredient.csv')
j = rec_ingr.join(recipes, on='recipe_id').join(products, on='product_id')

orders = pd.read_csv('data/orders.csv')
k = orders.join(j.set_index('recipe_id'), on='recipe_id', lsuffix='_order')
k['from_date'] = k['date'].dt.date + pd.to_timedelta(
    -np.random.randint(low=1, high=np.minimum(k['exp_date_days'], 365), size=k.shape[0]), unit='D')
