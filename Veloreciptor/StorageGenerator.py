import pandas as pd
import numpy as np

recipes = pd.read_csv('data/KK_recipes.csv').set_index('id')
products = pd.read_csv('data/products_table.csv').set_index('id')
rec_ingr = pd.read_csv('data/KK_recipe_ingredient.csv')
j = rec_ingr.join(recipes, on='recipe_id').join(products, on='product_id')

orders = pd.read_csv('data/orders.csv')
k = orders.join(j.set_index('recipe_id'), on='recipe_id', lsuffix='_order')
k['date'] = pd.to_datetime(k['date'])
k['to_date'] = k['date'].dt.date
k['from_date'] = k['to_date'] + pd.to_timedelta(
    -np.random.randint(low=1, high=np.minimum(k['exp_date_days'], 365), size=k.shape[0]), unit='D')

out = k.loc[:, ['product_id', 'quantity', 'price', 'exp_date_days', 'from_date', 'to_date']].reset_index(drop=True)
out = out.loc[-np.isnan(out['product_id']), :]

# random expired products
n = 20000
p = products.loc[np.random.choice(products.index, n), ['exp_date_days', 'price']]
p['quantity'] = np.random.geometric(0.025, n)
p['product_id'] = p.index
p['from_date'] = np.random.choice(k['from_date'], n)
p['to_date'] = p['from_date'] + pd.to_timedelta(p['exp_date_days'] + 1, unit='D')
last_date = max(k['to_date'])
p.loc[p['to_date'] > last_date, 'to_date'] = None

out = out.append(p).reset_index(drop=True)
out['id'] = out.index
out['entity_id'] = out.index

out.to_csv("data/warehouse.csv", index=False)

# + pk: warehouse_record_id
# + unikalny_kod_encji: entity_id
# + typ_produktu: product_id
# + ilość: quantity
# + cena: price
# + data_wazności: expiration_date
# + data_od: from_date
# + data_do: to_date
# + aktywność wpisu: activ
