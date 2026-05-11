-- =========================================
-- AIKIVAVIORA GreenMall Lab
-- Core Analytics Schema v0.1
-- =========================================

-- ============================================================
-- GREEN MALL: Core Database Schema
-- AIKIVAVIORA Core Analytics MVP
-- ============================================================

DROP TABLE IF EXISTS sales      CASCADE;
DROP TABLE IF EXISTS products   CASCADE;
DROP TABLE IF EXISTS customers  CASCADE;
DROP TABLE IF EXISTS employees  CASCADE;
DROP TABLE IF EXISTS cities     CASCADE;
DROP TABLE IF EXISTS categories CASCADE;
DROP TABLE IF EXISTS countries  CASCADE;

CREATE TABLE countries (
  "CountryID"    INT PRIMARY KEY,
  "CountryName"  TEXT NOT NULL,
  "CountryCode"  TEXT
);

CREATE TABLE categories (
  "CategoryID"   INT PRIMARY KEY,
  "CategoryName" TEXT NOT NULL
);

CREATE TABLE cities (
  "CityID"       INT PRIMARY KEY,
  "CityName"     TEXT NOT NULL,
  "Zipcode"      INT,
  "CountryID"    INT REFERENCES countries("CountryID")
);

CREATE TABLE employees (
  "EmployeeID"     INT PRIMARY KEY,
  "FirstName"      TEXT,
  "MiddleInitial"  TEXT,
  "LastName"       TEXT,
  "BirthDate"      TIMESTAMP,
  "Gender"         TEXT,
  "CityID"         INT REFERENCES cities("CityID"),
  "HireDate"       TIMESTAMP
);

CREATE TABLE customers (
  "CustomerID"     INT PRIMARY KEY,
  "FirstName"      TEXT,
  "MiddleInitial"  TEXT,
  "LastName"       TEXT,
  "CityID"         INT REFERENCES cities("CityID"),
  "Address"        TEXT
);

CREATE TABLE products (
  "ProductID"      INT PRIMARY KEY,
  "ProductName"    TEXT NOT NULL,
  "Price"          NUMERIC(10,4),
  "CategoryID"     INT REFERENCES categories("CategoryID"),
  "Class"          TEXT,
  "ModifyDate"     TIMESTAMP,
  "Resistant"      TEXT,
  "IsAllergic"     TEXT,
  "VitalityDays"   NUMERIC(10,1)
);

CREATE TABLE sales (
  "SalesID"            INT PRIMARY KEY,
  "SalesPersonID"      INT REFERENCES employees("EmployeeID"),
  "CustomerID"         INT REFERENCES customers("CustomerID"),
  "ProductID"          INT REFERENCES products("ProductID"),
  "Quantity"           INT,
  "Discount"           NUMERIC(5,2),
  "TotalPrice"         NUMERIC(12,2),
  "SalesDate"          TIMESTAMP,
  "TransactionNumber"  TEXT
);