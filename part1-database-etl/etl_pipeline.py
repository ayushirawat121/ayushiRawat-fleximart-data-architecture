from sqlalchemy import create_engine, text
import pandas as pd
from sqlalchemy import text
import os

#this is for data quality report
dq_report = {
    "customers": {},
    "products": {},
    "sales": {}
}

BASE_DIRECTORY = os.path.dirname(os.path.abspath(__file__))

#mysql connection sqlalchemy
engine = create_engine("mysql+pymysql://root:Test12345678@localhost:3306/fleximart")

# Read customers data
customers_df = pd.read_csv("./raw_data/customers_raw.csv",
                           dtype={"customer_id": "string", "phone": "string"},
                           keep_default_na=False)

# Read products data
products_df = pd.read_csv(
    "./raw_data/products_raw.csv",
    dtype={"product_id": "string", "category": "string"},
    keep_default_na=False)

# Read sales data
sales_df = pd.read_csv(
    "./raw_data/sales_raw.csv",
    dtype={
        "transaction_id": "string",
        "customer_id": "string",
        "product_id": "string",
        "status": "string"
    },
    keep_default_na=False)

dq_report["customers"]["records_processed"] = len(customers_df)
dq_report["products"]["records_processed"] = len(products_df)
dq_report["sales"]["records_processed"] = len(sales_df)

#method for standardizing the phone number----
def standardize_phone(phone):
    if pd.isna(phone):
        return None

    # Convert to string and keep digits only
    digits = "".join(filter(str.isdigit, str(phone)))

    # Always take the LAST 10 digits
    if len(digits) >= 10:
        digits = digits[-10:]
    else:
         # invalid phone number
        return None 

    return "+91-" + digits

#method for standardizing the categories in products table
def standardize_category(category):
    mapping = {
        "electronics": "Electronics",
        "fashion": "Fashion",
        "groceries": "Groceries"
    }
    if category is None:
        return None

    s = str(category).strip().lower()
    return mapping.get(s, s.title())

#method to standardize the date format
def to_yyyy_mm_dd(date_series: pd.Series) -> pd.Series:
    # Handles mixed formats like 2024-01-15, 15/01/2024, 01-22-2024, 03-25-2024 etc.
    return pd.to_datetime(date_series, errors="coerce", dayfirst=True).dt.strftime("%Y-%m-%d")


# ----------------------------
# TRANSFORM: Customers Data
# ----------------------------

def transform_customer_data(customers_df : pd.DataFrame, dq_report: dict) -> pd.DataFrame :
    df = customers_df.copy()

    before = len(df)
    df = df.drop_duplicates(subset="customer_id", keep="first")
    after = len(df)
    dq_report["customers"]["duplicates_removed"] = before - after

    missing_email = (df["email"].astype(str).str.strip() == "").sum()
    dq_report["customers"]["missing_values_handled"] = int(missing_email)

    #remove the duplicate customers by using the customer id
    df = df.drop_duplicates(subset="customer_id", keep="first")

    #handling the missing values in customer table
    df["email"] = df["email"].replace("", pd.NA)  # missing email -> NULL
    df["email"] = df["email"].fillna(df["customer_id"].str.lower() + "@unknown.com")
    df["first_name"] = df["first_name"].replace("", pd.NA)
    df["last_name"] = df["last_name"].replace("", pd.NA)
    df["city"] = df["city"].replace("", pd.NA)

    #standardize the phone number
    df["phone"] = df["phone"].apply(standardize_phone)

    # Convert registration_date to YYYY-MM-DD
    df["registration_date"] = to_yyyy_mm_dd(df["registration_date"])

    #add the surrogate key in the customer table
    df = df.reset_index(drop=True)
    df.insert(0, "customer_sk", df.index + 1)

    return df


# ----------------------------
# TRANSFORM: Products Data
# ----------------------------

def transform_products_data(products_df: pd.DataFrame, dq_report: dict) -> pd.DataFrame:
    df = products_df.copy()

    # --- duplicates removed ---
    before = len(df)
    df = df.drop_duplicates(subset="product_id", keep="first")
    after = len(df)
    dq_report["products"]["duplicates_removed"] = int(before - after)

    # --- missing values handled ---
    # missing price count BEFORE filling with 0
    missing_price = pd.to_numeric(df["price"], errors="coerce").isna().sum()
    dq_report["products"]["missing_values_handled"] = int(missing_price)

    # Standardize category names
    df["category"] = df["category"].apply(standardize_category)

    # Convert numeric columns + fill missing price with 0
    df["price"] = pd.to_numeric(df["price"], errors="coerce").fillna(0)

    df["stock_quantity"] = (
        pd.to_numeric(df["stock_quantity"], errors="coerce")
        .astype("Int64")
        .fillna(0)
    )

    # Add surrogate key
    df = df.reset_index(drop=True)
    df.insert(0, "product_sk", df.index + 1)

    return df

# ----------------------------
# TRANSFORM: Sales Data
# ----------------------------

def transform_sales_data(sales_df: pd.DataFrame, dq_report: dict) -> pd.DataFrame:
    df = sales_df.copy()

    # --- duplicates removed ---
    before = len(df)
    df = df.drop_duplicates(subset="transaction_id", keep="first")
    after = len(df)
    dq_report["sales"]["duplicates_removed"] = int(before - after)

    # --- missing values handled ---
    missing_customer = (df["customer_id"].astype(str).str.strip() == "").sum()
    missing_product = (df["product_id"].astype(str).str.strip() == "").sum()
    dq_report["sales"]["missing_values_handled"] = int(missing_customer + missing_product)

    # Handle missing customer_id/product_id (convert blanks -> NA)
    df["customer_id"] = df["customer_id"].replace("", pd.NA)
    df["product_id"] = df["product_id"].replace("", pd.NA)

    # drop rows missing critical fields
    df = df.dropna(subset=["customer_id", "product_id"])

    # Convert numeric columns
    df["quantity"] = pd.to_numeric(df["quantity"], errors="coerce").astype("Int64")
    df["unit_price"] = pd.to_numeric(df["unit_price"], errors="coerce")

    # drop rows where quantity or unit_price is missing/invalid
    df = df.dropna(subset=["quantity", "unit_price"])

    # Convert transaction_date to YYYY-MM-DD
    df["transaction_date"] = to_yyyy_mm_dd(df["transaction_date"])

    # Standardize status
    df["status"] = df["status"].str.strip().str.lower().str.capitalize()

    # Add surrogate key
    df = df.reset_index(drop=True)
    df.insert(0, "sales_sk", df.index + 1)

    return df


if __name__ == "__main__":
    customers_clean = transform_customer_data(customers_df, dq_report)
    products_clean = transform_products_data(products_df, dq_report)
    sales_clean = transform_sales_data(sales_df, dq_report)

# ----------------------------
#cleaning the data in db before performing data insertion
# ----------------------------
with engine.begin() as conn:
    conn.execute(text("SET FOREIGN_KEY_CHECKS = 0"))
    conn.execute(text("TRUNCATE TABLE order_items"))
    conn.execute(text("TRUNCATE TABLE orders"))
    conn.execute(text("TRUNCATE TABLE products"))
    conn.execute(text("TRUNCATE TABLE customers"))
    conn.execute(text("SET FOREIGN_KEY_CHECKS = 1"))


#next is to insert the data into database
#this method is used to load customers data into the database
def load_customers(customers_clean: pd.DataFrame, engine) -> dict:
    temp = customers_clean.copy()

    # DB constraint: email is UNIQUE NOT NULL
    temp["email"] = temp["email"].fillna(temp["customer_id"].str.lower() + "@unknown.com")

    insert_df = temp[[
        "first_name",
        "last_name",
        "email",
        "phone",
        "city",
        "registration_date"
    ]]

    insert_df.to_sql("customers", con=engine, if_exists="append", index=False)

    # Mapping business customer_id (C001) -> db customer_id (INT)
    with engine.connect() as conn:
        db_customers = pd.read_sql(text("SELECT customer_id, email FROM customers"), conn)

    merged = temp.merge(db_customers, on="email", how="left")
    customer_map = dict(zip(merged["customer_id_x"], merged["customer_id_y"]))

    return customer_map


#this method is used to load product data into the database
def load_products(products_clean: pd.DataFrame, engine) -> dict:
    temp = products_clean.copy()

    # DB constraint: price is NOT NULL and filling the value with 0
    temp["price"] = temp["price"].fillna(0)

    insert_df = temp[[
        "product_name",
        "category",
        "price",
        "stock_quantity"
    ]]

    insert_df.to_sql("products", con=engine, if_exists="append", index=False)

    # mapping product_id -> db product_id
    # Mapping uses product_name because DB table doesn't have business product_code.
    with engine.connect() as conn:
        db_products = pd.read_sql(text("SELECT product_id, product_name FROM products"), conn)

    merged = temp.merge(db_products, on="product_name", how="left")
    product_map = dict(zip(merged["product_id_x"], merged["product_id_y"]))

    return product_map

#insert orders and orders items into database
def load_orders_and_items_mysql(sales_clean: pd.DataFrame, engine, customer_map: dict, product_map: dict) -> None:
    df = sales_clean.copy()

    # Map business IDs -> DB IDs
    df["customer_id_int"] = df["customer_id"].map(customer_map)
    df["product_id_int"] = df["product_id"].map(product_map)

    # Keep only rows that can be inserted
    df = df.dropna(subset=["customer_id_int", "product_id_int", "transaction_date", "quantity", "unit_price"])
    df["customer_id_int"] = df["customer_id_int"].astype(int)
    df["product_id_int"] = df["product_id_int"].astype(int)
    df["quantity"] = df["quantity"].astype(int)
    df["unit_price"] = df["unit_price"].astype(float)

    # Calculate totals
    df["subtotal"] = (df["quantity"] * df["unit_price"]).round(2)

    insert_order_sql = text("""
        INSERT INTO orders (customer_id, order_date, total_amount, status)
        VALUES (:customer_id, :order_date, :total_amount, :status)
    """)

    insert_item_sql = text("""
        INSERT INTO order_items (order_id, product_id, quantity, unit_price, subtotal)
        VALUES (:order_id, :product_id, :quantity, :unit_price, :subtotal)
    """)

    # Use a transaction so it's all-or-nothing
    with engine.begin() as conn:
        for _, row in df.iterrows():
            # 1) Insert order and get generated order_id
            result = conn.execute(insert_order_sql, {
                "customer_id": row["customer_id_int"],
                "order_date": row["transaction_date"],  # must be YYYY-MM-DD (string is fine)
                "total_amount": float(row["subtotal"]),
                "status": row["status"] if pd.notna(row["status"]) else "Pending"
            })
            order_id = result.lastrowid  # ✅ MySQL-specific and reliable

            # 2) Insert order item
            conn.execute(insert_item_sql, {
                "order_id": order_id,
                "product_id": row["product_id_int"],
                "quantity": int(row["quantity"]),
                "unit_price": float(row["unit_price"]),
                "subtotal": float(row["subtotal"])
            })

    print(f"Inserted {len(df)} orders and {len(df)} order_items")

#method to generate the data quality report
def write_data_quality_report(dq_report, filepath):
    with open(filepath, "w", encoding="utf-8") as f:
        f.write("DATA QUALITY REPORT\n")
        f.write("=" * 50 + "\n\n")

        for name in ["customers", "products", "sales"]:
            f.write(f"{name.upper()} FILE\n")
            f.write(f"Number of records processed          : {dq_report[name].get('records_processed', 0)}\n")
            f.write(f"Number of duplicates removed         : {dq_report[name].get('duplicates_removed', 0)}\n")
            f.write(f"Number of missing values handled     : {dq_report[name].get('missing_values_handled', 0)}\n")
            f.write(f"Number of records loaded successfully: {dq_report[name].get('records_loaded_successfully', 0)}\n\n")

    print("data_quality_report.txt generated")


if __name__ == "__main__":
    customer_map = load_customers(customers_clean, engine)
    product_map = load_products(products_clean, engine)
    load_orders_and_items_mysql(sales_clean, engine, customer_map, product_map)

    print("Clean data inserted into MySQL successfully")
    

 #records loaded successfully
dq_report["customers"]["records_loaded_successfully"] = len(customers_clean)
dq_report["products"]["records_loaded_successfully"] = len(products_clean)
dq_report["sales"]["records_loaded_successfully"] = len(sales_clean)

#write the data quality report
report_path = os.path.join(BASE_DIRECTORY, "data_quality_report.txt")
write_data_quality_report(dq_report, report_path)




