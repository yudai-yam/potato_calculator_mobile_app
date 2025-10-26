
from datetime import datetime
from pathlib import Path
import pandas as pd
from conf import settings

def calculate_price(
    grams: float,
) -> int:
    """
    calculate the price of potatoes based on wight

    Parameters:
        grams: weight of potatoes in grams
    """
    
    if grams >= settings.discount_threshold_grams:
        temp = (grams / 100) * settings.price_100g_discounted
    else:
        temp = (grams / 100) * settings.price_100g
    
    return round(int(temp), -1)

def is_csv_empty(file_path: Path) -> bool:
    """
    Check if the CSV file is empty.

    Parameters:
        filename: name of the CSV file to check
    """
    
    try:
        df = pd.read_csv(file_path)  #read the CSV file

        if df.empty:  # Check if the DataFrame is empty
            return True
        else:
            return False
    except pd.errors.EmptyDataError:
        return True
    except FileNotFoundError:
        print("File not found.")
        return True


def save_sales(grams: int, price: int, filename: str = "sales.csv") -> None:
    """
    Save the sales record to a file.

    Parameters:
        grams: weight of potatoes in grams
        price: calculated price
        filename: name of the file to save the record
    """
    date = datetime.now().strftime("%x")
    time = datetime.now().strftime("%X")

    data = {"date": date, "time": time, "grams": grams, "price": price}

    file_path = Path(filename)


    data_series = pd.Series(data)

    if is_csv_empty(file_path):
        data_series.to_frame().T.to_csv(file_path, mode="a", index=False)
    else:
        data_series.to_frame().T.to_csv(file_path, mode="a", header=False, index=False)

