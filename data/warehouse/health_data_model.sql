-- Create schema for healthcare analytics

-- 1. Table: locations
CREATE TABLE locations (
    location_id SERIAL PRIMARY KEY,
    stateabbr VARCHAR(2) NOT NULL,
    statedesc VARCHAR(255) NOT NULL,
    locationname VARCHAR(255) NOT NULL,
    geolocation POINT
);

-- 2. Table: categories
CREATE TABLE categories (
    category_id SERIAL PRIMARY KEY,
    category VARCHAR(255) NOT NULL,
    measure VARCHAR(255) NOT NULL,
    short_question_text VARCHAR(255)
);

-- 3. Table: metrics
CREATE TABLE metrics (
    metric_id SERIAL PRIMARY KEY,
    year INT NOT NULL,
    data_value NUMERIC(10, 2),
    low_confidence_limit NUMERIC(10, 2),
    high_confidence_limit NUMERIC(10, 2),
    data_value_type VARCHAR(255),
    totalpopulation BIGINT,
    totalpop18plus BIGINT,
    location_id INT REFERENCES locations(location_id),
    category_id INT REFERENCES categories(category_id)
);

-- 4. Sample Insert Queries
-- Insert sample data into locations
INSERT INTO locations (stateabbr, statedesc, locationname, geolocation)
VALUES 
('AL', 'Alabama', 'Autauga', '(86.642816, 32.535001)'),
('CA', 'California', 'Los Angeles', '(-118.2437, 34.0522)');

-- Insert sample data into categories
INSERT INTO categories (category, measure, short_question_text)
VALUES 
('Prevention', 'Current lack of health insurance among adults', 'Health Insurance'),
('Health Outcomes', 'Arthritis among adults', 'Arthritis');

-- Insert sample data into metrics
INSERT INTO metrics (year, data_value, low_confidence_limit, high_confidence_limit, data_value_type, totalpopulation, totalpop18plus, location_id, category_id)
VALUES 
(2022, 7.1, 6.2, 7.9, 'Crude prevalence', 59759, 45878, 1, 1),
(2022, 34.5, 33.8, 35.3, 'Crude prevalence', 59759, 45878, 1, 2);
