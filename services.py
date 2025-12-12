from models import db, Product, ProductType, MaterialType, Workshop, ProductWorkshop
from sqlalchemy import func

def calculate_production_time(product_id):
    """Рассчитывает общее время изготовления продукции"""
    try:
        total_time = db.session.query(func.sum(ProductWorkshop.time_in_workshop))\
            .filter(ProductWorkshop.product_id == product_id)\
            .scalar() or 0
        
        return round(float(total_time))
    except Exception as e:
        print(f"Ошибка при расчете времени производства: {str(e)}")
        return 0

def calculate_raw_material(product_type_id, material_type_id, quantity, param1, param2):
    """Рассчитывает количество сырья с учетом потерь"""
    try:
        # Проверяем существование типов продукции и материала
        product_type = ProductType.query.get(product_type_id)
        material_type = MaterialType.query.get(material_type_id)
        
        if not product_type:
            print(f"Тип продукции с ID {product_type_id} не найден")
            return -1
        
        if not material_type:
            print(f"Тип материала с ID {material_type_id} не найден")
            return -1
        
        # Проверяем параметры
        if param1 <= 0:
            print(f"Ошибка: Параметр 1 должен быть положительным: {param1}")
            return -1
            
        if param2 <= 0:
            print(f"Ошибка: Параметр 2 должен быть положительным: {param2}")
            return -1
            
        if quantity <= 0:
            print(f"Ошибка: Количество должно быть положительным: {quantity}")
            return -1
        
        print(f"Расчет для: {product_type.name}, материал: {material_type.name}")
        print(f"Входные данные: quantity={quantity}, param1={param1}, param2={param2}")
        
        # Проверяем коэффициенты
        if product_type.coefficient is None:
            print("Ошибка: Коэффициент типа продукции не установлен")
            return -1
        
        material_loss = float(material_type.waste_percentage)
        coefficient = float(product_type.coefficient)
        
        print(f"Коэффициент типа продукции: {coefficient}")
        print(f"Процент потерь материала: {material_loss}")
        
        # Основной расчет
        area = param1 * param2
        base_material = area * coefficient
        print(f"Базовая площадь: {area}")
        print(f"Базовое количество сырья: {base_material}")
        
        # Рассчитываем коэффициент потерь
        waste_factor = 1.0 + material_loss
        print(f"Коэффициент потерь: {waste_factor}")
        
        # Рассчитываем общее количество с учетом потерь
        total_material = base_material * waste_factor * quantity
        print(f"Итоговое количество сырья до округления: {total_material}")
        
        # Возвращаем округленное вверх целое число
        result = int(total_material + 0.999)  # Округление вверх
        print(f"Округленный результат: {result}")
        return result
        
    except Exception as e:
        print(f"КРИТИЧЕСКАЯ ОШИБКА в расчете: {e}")
        import traceback
        traceback.print_exc()
        return -1