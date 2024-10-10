import pandas as pd

def load_data(csv_path):
    df = pd.read_csv(csv_path)
    df["T1"] = df["T1"].str.strip()
    df["T2"] = df["T2"].str.strip()
    df["T1"] = df["T1"].str.replace("Bilibili Gaming", "BLG")
    df["T2"] = df["T2"].str.replace("Bilibili Gaming", "BLG")
    return df
