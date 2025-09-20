SET search_path TO content;


INSERT INTO category (id, name, description)
VALUES
    ('a1f4e8bf-61e3-4f42-8be1-5318dfc4a0a1', 'Electronics', 'Various electronic products'),
    ('b2f4e8bf-61e3-4f42-8be1-5318dfc4a0b2', 'Home Appliances', 'Products for home and kitchen'),
    ('c3f4e8bf-61e3-4f42-8be1-5318dfc4a0c3', 'Books', 'Collection of books in various genres');


INSERT INTO subcategory (id, name, description, category_id)
VALUES
    ('d1f4e8bf-61e3-4f42-8be1-5318dfc4a0d1', 'Mobile Phones', 'Smartphones and accessories', 'a1f4e8bf-61e3-4f42-8be1-5318dfc4a0a1'),
    ('e2f4e8bf-61e3-4f42-8be1-5318dfc4a0e2', 'Laptops', 'Portable computers and accessories', 'a1f4e8bf-61e3-4f42-8be1-5318dfc4a0a1'),
    ('f3f4e8bf-61e3-4f42-8be1-5318dfc4a0f3', 'Washing Machines', 'Automatic and semi-automatic washers', 'b2f4e8bf-61e3-4f42-8be1-5318dfc4a0b2'),
    ('f4f4e8bf-61e3-4f42-8be1-5318dfc4a0f4', 'Refrigerators', 'Fridges and cooling appliances', 'b2f4e8bf-61e3-4f42-8be1-5318dfc4a0b2'),
    ('c5f4e8bf-61e3-4f42-8be1-5318dfc4a0c5', 'Fiction', 'Books in the fiction genre', 'c3f4e8bf-61e3-4f42-8be1-5318dfc4a0c3'),
    ('a6f4e8bf-61e3-4f42-8be1-5318dfc4a0a6', 'Non-fiction', 'Books in the non-fiction genre', 'c3f4e8bf-61e3-4f42-8be1-5318dfc4a0c3');


INSERT INTO product (id, name, description, price, photo_link, subcategory_id)
VALUES
    ('ae144aac-d2bc-45a0-8979-70ee3eae5d09', 'iPhone 12', 'Latest Apple smartphone', 799.99, 'photos/img.png', 'd1f4e8bf-61e3-4f42-8be1-5318dfc4a0d1'),
    ('b94fbc73-22ea-46cc-91cf-a900e567ea5d', 'MacBook Air', 'Apple laptop with M1 chip', 999.99, 'photos/img.png', 'e2f4e8bf-61e3-4f42-8be1-5318dfc4a0e2'),
    ('45af658c-acf3-44ef-b98a-5c589e34e185', 'Samsung Galaxy S21', 'Samsung smartphone with high-end features', 699.99, 'photos/img.png', 'd1f4e8bf-61e3-4f42-8be1-5318dfc4a0d1'),
    ('0f88d61e-3a19-4993-af3c-ab4f79f4079f', 'LG Washing Machine', 'High-efficiency washing machine', 499.99, 'photos/img.png', 'f3f4e8bf-61e3-4f42-8be1-5318dfc4a0f3'),
    ('5a71c069-1a4e-483c-b3f6-3ddf2c3efb05', 'Samsung Refrigerator', 'Energy-efficient refrigerator', 799.99, 'photos/img.png', 'f4f4e8bf-61e3-4f42-8be1-5318dfc4a0f4'),
    ('cee0cafd-b8ce-4225-adcd-02e44adb5db4', 'To Kill a Mockingbird', 'Harper Lee novel', 14.99, 'photos/img.png', 'c5f4e8bf-61e3-4f42-8be1-5318dfc4a0c5'),
    ('88ef0a41-50fa-4294-a44a-e4325ec449e9', 'Sapiens', 'Yuval Noah Hararis book on human history', 19.99, 'photos/img.png', 'a6f4e8bf-61e3-4f42-8be1-5318dfc4a0a6');
