import numpy as np
import pandas as pd


def random_dates(start, end, n):
    n_days = (end - start).days + 1
    return pd.to_timedelta(np.random.randint(0, n_days, n), unit='D') + start


def random_times(n, dates):
    start = 9 * 60
    middle = [15 * 60 if date.weekday() <= 4 else 18 * 60 for date in dates]
    end = 21 * 60
    return pd.to_timedelta(np.random.triangular(left=start, mode=middle, right=end, size=n).astype(np.int64), unit='m')


recipes = pd.read_csv('data/KK_recipes.csv')
recipes['frequency'] = np.random.geometric(0.4, recipes.shape[0])
recipes['default_price'] = np.round(np.random.uniform(22.0, 48.0, recipes.shape[0]), 2)

# order generator
n = 18715
start_date = pd.to_datetime('2018-10-13')
end_date = pd.to_datetime('2020-06-06')
orders = pd.DataFrame(columns=['id', 'recipe_id', 'price'])
orders['recipe_id'] = np.random.choice(recipes['id'], n, p=recipes['frequency']/np.sum(recipes['frequency']))
orders['price'] = [recipes[recipes['id'] == i].iloc[0]['default_price'] for i in orders['recipe_id']]
orders['price'] *= 2

# datetime generator
orders['date'] = random_dates(start_date, end_date, orders.shape[0])
orders['date'] += random_times(orders.shape[0], orders['date'])
orders = orders.sort_values('date').reset_index(drop=True)
orders['id'] = orders.index

# cheap fridays
orders.loc[[i.weekday() == 4 for i in orders['date']], 'price'] *= 0.75

orders.to_csv("data/orders.csv", index=False)
