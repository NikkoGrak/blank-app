

import pandas as pd
from customer import Customer

def read_waypoints_from_excel(file_path):
    df = pd.read_excel(file_path)
    df = df[['Kota', 'Kelurahan', 'Nama Toko', 'Latitude', 'Longitude']].iloc[0:57].dropna()
    waypoints = [Customer(row['Kota'], row['Kelurahan'], row['Nama Toko'], row['Latitude'], row['Longitude']) for _, row in df.iterrows()]
    return waypoints
