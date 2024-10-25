-- TABLE
CREATE TABLE Category (
    Category_ID INT(10) PRIMARY KEY,
    Category_Name VARCHAR(40),
    Description VARCHAR(40)
);
CREATE TABLE Customer (
    Customer_ID INT(10) PRIMARY KEY,
    First_Name VARCHAR(40),
    Last_Name VARCHAR(40),
    Address VARCHAR(40),
    Phone INT(10),
    Email VARCHAR(40),
    Staff_ID INT(10),
    FOREIGN KEY (Staff_ID) REFERENCES Staff(Staff_ID)
);
CREATE TABLE `Order`( 
  Order_ID INT(10) PRIMARY KEY, 
  Date_of_Order DATE, 
  Order_Details VARCHAR(40), 
  Customer_ID INT(10), 
  FOREIGN KEY (Customer_ID) REFERENCES Customer(Customer_ID) 
);
CREATE TABLE Order_Detail (
    Order_Detail_ID INT(10) PRIMARY KEY,
    Unit_Price FLOAT(8,1),
    Size INT(10),
    Quantity INT(10),
    Discount FLOAT(8,1),
    Total FLOAT(8,1),
    Date DATE,
    Product_ID VARCHAR(40),
    Order_ID INT(10),
    Bill_number INT(10),
    FOREIGN KEY (Product_ID) REFERENCES Product(Product_ID),  -- Assuming the Product table and Product_ID as the referenced column
    FOREIGN KEY (Order_ID) REFERENCES `Order`(Order_ID),       -- Assuming the Orders table and Order_ID as the referenced column
    FOREIGN KEY (Bill_number) REFERENCES Payment(Bill_number)       -- Assuming the Bill table and Bill_ID as the referenced column
);
CREATE TABLE Payment (
    Bill_number INT(10) PRIMARY KEY,
    Payment_Type VARCHAR(40),
    Other_Details VARCHAR(40)
);
CREATE TABLE Product (
    Product_ID VARCHAR(40) PRIMARY KEY,
    Product_Name VARCHAR(40),
    Product_description VARCHAR(40),
    Product_unit VARCHAR(40),
    Product_Price FLOAT(8,1),
    Product_quantity INT(10),
    Product_Status INT(10),
    Other_Details VARCHAR(40),
    Supplier_ID INT(10),
    Category_ID INT(10),
    FOREIGN KEY (Supplier_ID) REFERENCES Supplier(Supplier_ID),
    FOREIGN KEY (Category_ID) REFERENCES Category(Category_ID)
);
CREATE TABLE Role (
    Role_ID INT(10) PRIMARY KEY,
    Role_Name VARCHAR(40),
    Description VARCHAR(40)
);
CREATE TABLE Staff (
    Staff_ID INT(10) PRIMARY KEY,
    First_Name VARCHAR(40),
    Last_Name VARCHAR(40),
    Address VARCHAR(40),
    Phone INT(10),
    Email VARCHAR(40),
    UserName VARCHAR(40),
    Password VARCHAR(40),
    Role_ID INT(10),
    FOREIGN KEY (Role_ID) REFERENCES Roles(Role_ID)
);
CREATE TABLE Supplier (
    Supplier_ID INT(10) PRIMARY KEY,
    Name VARCHAR(40),
    Address VARCHAR(40),
    Phone INT(10),
    Fax INT(10),
    Email VARCHAR(40),
    Other_Details VARCHAR(40)
);
 
-- INDEX
 
-- TRIGGER
 
-- VIEW
 
