"""
trucking_app - database.py
==========================
Creates and manages the SQLite database for trucking_app.
Run this once to initialize the database, or any time you
want to reset it back to a clean state.
 
Usage:
    python database.py
"""
 
import sqlite3
import os
from datetime import datetime
 
# --- Configuration ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH  = os.path.join(BASE_DIR, "data", "trucking_app.db")
 
 
def get_connection() -> sqlite3.Connection:
    """
    Return a connection to the database with foreign key support enabled.
    Call this from any other module that needs to read or write data.
    """
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row   # rows behave like dicts
    conn.execute("PRAGMA foreign_keys = ON")
    return conn
 
 
def create_tables(conn: sqlite3.Connection) -> None:
    """
    Create all tables if they do not already exist.
    Safe to run multiple times — existing data is never touched.
    """
    cursor = conn.cursor()
 
    # ------------------------------------------------------------------
    # TRUCKS
    # One row per physical truck.  Even if you only have one truck today,
    # this makes trucking_app ready to sell to fleets.
    # ------------------------------------------------------------------
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS trucks (
            truck_id        INTEGER PRIMARY KEY AUTOINCREMENT,
            year            INTEGER NOT NULL,
            make            TEXT    NOT NULL,
            model           TEXT    NOT NULL,
            vin             TEXT    UNIQUE,
            plate           TEXT,
            odometer_start  INTEGER DEFAULT 0,
            carrier         TEXT,           -- e.g. Mercer Transportation
            created_at      TEXT    DEFAULT (datetime('now'))
        )
    """)
 
    # ------------------------------------------------------------------
    # LOADS
    # Every load you pulled.  rate_per_mile * miles should equal gross_pay
    # but we store both so you can spot discrepancies.
    # ------------------------------------------------------------------
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS loads (
            load_id         INTEGER PRIMARY KEY AUTOINCREMENT,
            truck_id        INTEGER NOT NULL REFERENCES trucks(truck_id),
            load_number     TEXT,           -- Mercer load / pro number
            pickup_date     TEXT NOT NULL,  -- YYYY-MM-DD
            delivery_date   TEXT,           -- YYYY-MM-DD
            origin          TEXT NOT NULL,  -- city, state
            destination     TEXT NOT NULL,  -- city, state
            miles           REAL,
            rate_per_mile   REAL,
            gross_pay       REAL,
            commodity       TEXT,
            notes           TEXT,
            created_at      TEXT DEFAULT (datetime('now'))
        )
    """)
 
    # ------------------------------------------------------------------
    # SETTLEMENTS
    # Your Mercer weekly settlement sheets.
    # net_pay = gross_revenue - deductions
    # ------------------------------------------------------------------
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS settlements (
            settlement_id   INTEGER PRIMARY KEY AUTOINCREMENT,
            truck_id        INTEGER NOT NULL REFERENCES trucks(truck_id),
            period_start    TEXT NOT NULL,  -- YYYY-MM-DD
            period_end      TEXT NOT NULL,  -- YYYY-MM-DD
            gross_revenue   REAL,
            deductions      REAL DEFAULT 0,
            net_pay         REAL,
            source_file     TEXT,           -- original PDF/CSV filename
            notes           TEXT,
            created_at      TEXT DEFAULT (datetime('now'))
        )
    """)
 
    # ------------------------------------------------------------------
    # EXPENSES
    # Every dollar going out.  load_id is optional — some expenses
    # (insurance, truck payment) are not tied to a single load.
    # ------------------------------------------------------------------
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS expenses (
            expense_id      INTEGER PRIMARY KEY AUTOINCREMENT,
            truck_id        INTEGER NOT NULL REFERENCES trucks(truck_id),
            load_id         INTEGER REFERENCES loads(load_id),
            date            TEXT NOT NULL,  -- YYYY-MM-DD
            category        TEXT NOT NULL,  -- see EXPENSE_CATEGORIES below
            amount          REAL NOT NULL,
            description     TEXT,
            vendor          TEXT,
            receipt_file    TEXT,           -- path to scanned receipt
            source          TEXT DEFAULT 'manual',  -- manual / import / ocr
            created_at      TEXT DEFAULT (datetime('now'))
        )
    """)
 
    # ------------------------------------------------------------------
    # FUEL_STOPS
    # Fuel gets its own table so we can track MPG, state totals, and
    # cost-per-gallon trends over your 5 years of data.
    # ------------------------------------------------------------------
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS fuel_stops (
            fuel_id         INTEGER PRIMARY KEY AUTOINCREMENT,
            truck_id        INTEGER NOT NULL REFERENCES trucks(truck_id),
            date            TEXT NOT NULL,  -- YYYY-MM-DD
            location        TEXT,           -- city
            state           TEXT,           -- 2-letter state code
            gallons         REAL,
            price_per_gal   REAL,
            total_cost      REAL,
            odometer        INTEGER,
            card_used       TEXT,           -- Comdata, EFS, cash, etc.
            receipt_file    TEXT,
            created_at      TEXT DEFAULT (datetime('now'))
        )
    """)
 
    # ------------------------------------------------------------------
    # EXPENSE_CATEGORIES lookup table
    # Keeps category names consistent across the whole database.
    # ------------------------------------------------------------------
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS expense_categories (
            category_id     INTEGER PRIMARY KEY AUTOINCREMENT,
            name            TEXT UNIQUE NOT NULL,
            description     TEXT
        )
    """)
 
    conn.commit()
    print("  All tables created (or already exist).")
 
 
def seed_categories(conn: sqlite3.Connection) -> None:
    """
    Insert the standard trucking expense categories.
    Uses INSERT OR IGNORE so re-running this is always safe.
    """
    categories = [
        ("Fuel",            "Diesel fuel purchases"),
        ("Maintenance",     "Oil changes, tires, repairs, parts"),
        ("Insurance",       "Truck, cargo, occupational accident"),
        ("Permits",         "Oversize, overweight, state permits"),
        ("Tolls",           "Turnpike and highway tolls"),
        ("Scales",          "Weigh station fees"),
        ("Lumper",          "Loading and unloading labor fees"),
        ("Parking",         "Truck stop and secured parking"),
        ("Food",            "Meals while on the road"),
        ("Communication",   "Phone, ELD, Qualcomm, satellite"),
        ("Truck Payment",   "Monthly truck note / lease payment"),
        ("Escrow",          "Carrier escrow deductions"),
        ("Deadhead",        "Miles driven without a load"),
        ("Miscellaneous",   "Any expense that does not fit above"),
    ]
 
    conn.executemany(
        "INSERT OR IGNORE INTO expense_categories (name, description) VALUES (?, ?)",
        categories
    )
    conn.commit()
    print(f"  {len(categories)} expense categories loaded.")
 
 
def initialize_database() -> None:
    """
    Full initialization:  create tables → seed categories → done.
    """
    print("\n=== trucking_app database setup ===")
    print(f"Database path: {DB_PATH}\n")
 
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
 
    with get_connection() as conn:
        create_tables(conn)
        seed_categories(conn)
 
    print("\nDatabase is ready.")
    print("Next step: run  python add_truck.py  to enter your truck info.")
 
 
# --- Entry point ---
if __name__ == "__main__":
    initialize_database()