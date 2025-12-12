import pandas as pd
from app import app, db
from models import ProductType, MaterialType, Workshop, Product, ProductWorkshop
import re

def import_data():
    with app.app_context():
        # Очистка существующих данных
        print("Очистка существующих данных...")
        db.session.query(ProductWorkshop).delete()
        db.session.query(Product).delete()
        db.session.query(Workshop).delete()
        db.session.query(MaterialType).delete()
        db.session.query(ProductType).delete()
        db.session.commit()
        
        # Импорт типов продукции
        print("Импорт типов продукции...")
        product_types_df = pd.read_excel('Product_type_import.xlsx')
        for _, row in product_types_df.iterrows():
            pt = ProductType(
                name=row['Тип продукции'],
                coefficient=float(row['Коэффициент типа продукции'])
            )
            db.session.add(pt)
        db.session.commit()
        
        # Импорт типов материалов
        print("Импорт типов материалов...")
        material_types_df = pd.read_excel('Material_type_import.xlsx')
        for _, row in material_types_df.iterrows():
            # Обработка процента потерь: конвертируем "0.80%" в 0.008
            waste_str = str(row['Процент потерь сырья']).strip()
            
            # Извлекаем числовое значение из строки
            match = re.search(r'[\d.,]+', waste_str)
            if match:
                # Заменяем запятую на точку для корректного преобразования
                waste_value = match.group().replace(',', '.')
                waste_percent = float(waste_value)
                
                # Если значение больше 1, это вероятно проценты (0.80 -> 0.8%)
                # Если значение меньше 1, это уже десятичная дробь (0.008)
                if waste_percent >= 1:
                    waste_decimal = waste_percent / 100.0
                else:
                    waste_decimal = waste_percent
                
                # Если значение в пределах 0-10, считаем, что это проценты
                if 0 < waste_percent <= 10:
                    waste_decimal = waste_percent / 100.0
            else:
                waste_decimal = 0.0
            
            print(f"Материал: {row['Тип материала']}, исходное значение: '{waste_str}', итоговое значение: {waste_decimal}")
            
            mt = MaterialType(
                name=row['Тип материала'],
                waste_percentage=waste_decimal
            )
            db.session.add(mt)
        db.session.commit()
        
        # Импорт цехов
        print("Импорт цехов...")
        workshops_df = pd.read_excel('Workshops_import.xlsx')
        workshop_names = workshops_df['Название цеха'].unique()
        
        for name in workshop_names:
            name_clean = str(name).strip()
            if not name_clean:
                continue
                
            w = Workshop(
                name=name_clean,
                worker_count=5  # Стандартное количество работников
            )
            db.session.add(w)
        db.session.commit()
        
        # Импорт продукции
        print("Импорт продукции...")
        products_df = pd.read_excel('Products_import.xlsx')
        
        for _, row in products_df.iterrows():
            # Находим соответствующие типы
            product_type = ProductType.query.filter_by(name=row['Тип продукции']).first()
            material_type = MaterialType.query.filter_by(name=row['Основной материал']).first()
            
            if product_type and material_type:
                p = Product(
                    article=str(row['Артикул']),
                    product_type_id=product_type.id,
                    name=row['Наименование продукции'],
                    min_cost_for_partner=float(row['Минимальная стоимость для партнера']),
                    main_material_id=material_type.id,
                    parameter1=1.0,  # Значение по умолчанию
                    parameter2=1.0   # Значение по умолчанию
                )
                db.session.add(p)
        db.session.commit()
        
        # Импорт связей продукции и цехов
        print("Импорт связей продукции и цехов...")
        product_workshops_df = pd.read_excel('Product_workshops_import.xlsx')
        
        for _, row in product_workshops_df.iterrows():
            # Находим продукт и цех
            product_name = row['Наименование продукции']
            workshop_name = row['Название цеха']
            
            product = Product.query.filter_by(name=product_name).first()
            workshop = Workshop.query.filter_by(name=workshop_name).first()
            
            if product and workshop:
                time_in_workshop = float(row['Время изготовления, ч'])
                pw = ProductWorkshop(
                    product_id=product.id,
                    workshop_id=workshop.id,
                    time_in_workshop=time_in_workshop,
                    worker_count=3  # Стандартное количество работников
                )
                db.session.add(pw)
        db.session.commit()
        print("Импорт данных успешно завершен!")

if __name__ == '__main__':
    import_data()