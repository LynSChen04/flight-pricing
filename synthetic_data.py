import pandas as pd
import random
import numpy as np
from datetime import timedelta, datetime

airports = ['JFK', 'LAX', 'ORD', 'DFW', 'SEA', 'MIA', 'BOS']
airlines = ['Delta', 'United', 'American', 'Southwest', 'AirCanada','JetBlue', 'Alaska Airlines', 'Spirit Airlines', 'Frontier Airlines']
classes = ['Economy', 'Business']
base_date = datetime.today()

def generate_flight_data(n=500):
    data = []
    for _ in range(n):
        origin = random.choice(airports)
        dest = random.choice([a for a in airports if a != origin])
        departure_date = base_date + timedelta(days=random.randint(1, 120))
        search_date = departure_date - timedelta(days=random.randint(1, 90))
        price = round(random.uniform(100, 1000), 2)
        airline = random.choice(airlines)
        cabin_class = random.choice(classes)
        stops = random.choice([0, 1, 2])
        data.append({
            'origin': origin,
            'destination': dest,
            'departure_date': departure_date.date(),
            'search_date': search_date.date(),
            'price': price,
            'airline': airline,
            'cabin_class': cabin_class,
            'number_of_stops': stops
        })
    return pd.DataFrame(data)

df = generate_flight_data()
df.to_csv('synthetic_flight_prices.csv', index=False)