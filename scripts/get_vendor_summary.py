import pandas as pd
import sqlite3
import logging
from ingestion_db import ingest_db
import time

logging.basicConfig(
    filename = "./assets/logs/get_vendor_summary.log",
    level = logging.DEBUG,
    format = "%(asctime)s - %(levelname)s - %(message)s",
    filemode = "a",
    force = True
)

def create_vendor_summary(conn):
    '''This function merges different tables to get the overall vendor summary and adding new columns in the resultant data'''
    vendor_sales_summary = pd.read_sql_query("""
    WITH 
        FreightSummary AS (
            SELECT
                VendorNumber, 
                SUM(Freight) AS FreightCost
            FROM
                vendor_invoice
            GROUP BY
                VendorNumber
            ),
    
        PurchaseSummary AS (
            SELECT
                p.VendorNumber,
                p.VendorName,
                p.Brand,
                p.Description,
                p.PurchasePrice,
                pp.Price AS ActualPrice,
                pp.Volume,
                SUM(p.Quantity) AS TotalPurchaseQuantity,
                SUM(p.Dollars) AS TotalPurchaseDollars
            FROM
                purchases p
            JOIN
                purchase_prices pp
            ON
                p.Brand = pp.Brand
            WHERE
                p.PurchasePrice > 0
            GROUP BY
                p.vendorNumber,
                p.VendorName,
                p.Brand,
                p.Brand,
                p.Description,
                p.PurchasePrice,
                pp.Price,
                pp.Volume
            ),
            
        SalesSummary AS (
            SELECT
                s.VendorNo,
                s.Brand,
                SUM(s.SalesDollars) AS TotalSalesDollars,
                SUM(s.SalesPrice) as TotalSalesPrice,
                SUM(s.SalesQuantity) as TotalSalesQuantity,
                SUM(s.ExciseTax) as TotalExciseTax
            FROM 
                sales s
            GROUP BY 
                s.VendorNo, s.Brand
                )
                
    SELECT
        ps.VendorNumber,
        ps.VendorName,
        ps.Brand,
        ps.Description,
        ps.PurchasePrice,
        ps.ActualPrice,
        ps.Volume, 
        ps.TotalPurchaseQuantity,
        ps.TotalPurchaseDollars,
        ss.TotalSalesQuantity,
        ss.TotalSalesDollars,
        ss.TotalSalesPrice,
        ss.TotalExciseTax,
        fs.FreightCost
    From
        PurchaseSummary ps
    LEFT JOIN
        SalesSummary ss
        ON ps.Brand = ss.Brand 
        AND ps.VendorNumber = ss.VendorNo
    LEFT JOIN
        FreightSummary fs
        ON ps.VendorNumber = fs.VendorNumber
    ORDER BY
        ps.TotalPurchaseDollars DESC
    """, conn)
    return vendor_sales_summary

def clean_data(df):
    '''This function cleans the data'''
    df['Volume'] = df['Volume'].astype('float64')
    df['VendorName'] = df['VendorName'].str.strip()
    df['Description'] = df['Description'].str.strip()
    df.fillna(0, inplace = True)

    df['GrossProfit'] = df['TotalSalesDollars'] - df['TotalPurchaseDollars']
    df['ProfitMargin'] = (df['GrossProfit'] / df['TotalSalesDollars']) * 100
    df['StockTurnover'] = df['TotalSalesQuantity'] / df['TotalPurchaseQuantity']
    df['SalestoPurchaseRatio'] = df['TotalSalesDollars'] / df['TotalPurchaseDollars']
    return df


if __name__ == '__main__':
    conn = sqlite3.connect('inventory.db')
    start_time = time.time()
    logging.info('Creating Vendor Summary Table....')
    summary_df = create_vendor_summary(conn)
    logging.info(summary_df.head())

    logging.info('Cleaning Data....')
    clean_df = clean_data(summary_df)
    logging.info(clean_df.head())

    logging.info('Ingesting Data....')
    ingest_db(clean_df, 'vendor_sales_summary', conn)
    end_time = time.time()
    total_time = (end_time - start_time)/60
    logging.info('Completed')
    logging.info(f'\nTotal time taken: {total_time} minutes')