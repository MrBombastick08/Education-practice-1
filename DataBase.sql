
-- Создание базы данных для мебельной компании "Комфорт"

-- Таблица: Типы продукции
CREATE TABLE product_types (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE,
    coefficient DECIMAL(5, 2) NOT NULL DEFAULT 1.0
);

-- Таблица: Типы материалов
CREATE TABLE material_types (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE,
    waste_percentage DECIMAL(5, 2) NOT NULL DEFAULT 0.0
);

-- Таблица: Цеха
CREATE TABLE workshops (
    id SERIAL PRIMARY KEY,
    name VARCHAR(200) NOT NULL UNIQUE,
    worker_count INTEGER NOT NULL DEFAULT 0
);

-- Таблица: Продукция
CREATE TABLE products (
    id SERIAL PRIMARY KEY,
    article VARCHAR(50) UNIQUE NOT NULL,
    product_type_id INTEGER NOT NULL,
    name VARCHAR(200) NOT NULL,
    description TEXT,
    image_path VARCHAR(255),
    min_cost_for_partner DECIMAL(10, 2) NOT NULL CHECK (min_cost_for_partner >= 0),
    package_length DECIMAL(10, 2),
    package_width DECIMAL(10, 2),
    package_height DECIMAL(10, 2),
    weight_without_package DECIMAL(10, 2),
    weight_with_package DECIMAL(10, 2),
    certificate_path VARCHAR(255),
    standard_number VARCHAR(50),
    production_time DECIMAL(10, 2) NOT NULL DEFAULT 0,
    cost_price DECIMAL(10, 2),
    workshop_number INTEGER,
    worker_count_for_production INTEGER,
    main_material_id INTEGER,
    parameter1 DECIMAL(10, 2),
    parameter2 DECIMAL(10, 2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (product_type_id) REFERENCES product_types(id) ON DELETE CASCADE,
    FOREIGN KEY (main_material_id) REFERENCES material_types(id) ON DELETE SET NULL
);

-- Таблица: Связь продукции с цехами (многие ко многим)
CREATE TABLE product_workshops (
    id SERIAL PRIMARY KEY,
    product_id INTEGER NOT NULL,
    workshop_id INTEGER NOT NULL,
    time_in_workshop DECIMAL(10, 2) NOT NULL DEFAULT 0,
    worker_count INTEGER NOT NULL DEFAULT 1,
    FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE CASCADE,
    FOREIGN KEY (workshop_id) REFERENCES workshops(id) ON DELETE CASCADE,
    UNIQUE(product_id, workshop_id)
);

-- Создание индексов для ускорения запросов
CREATE INDEX idx_products_article ON products(article);
CREATE INDEX idx_products_type ON products(product_type_id);
CREATE INDEX idx_product_workshops_product ON product_workshops(product_id);
CREATE INDEX idx_product_workshops_workshop ON product_workshops(workshop_id);

-- Комментарии к таблицам
COMMENT ON TABLE product_types IS 'Типы продукции с коэффициентами для расчета';
COMMENT ON TABLE material_types IS 'Типы материалов с процентом потерь';
COMMENT ON TABLE workshops IS 'Цеха производства';
COMMENT ON TABLE products IS 'Продукция компании';
COMMENT ON TABLE product_workshops IS 'Связь продукции с цехами и время производства';