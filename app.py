from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from models import db, Product, ProductType, MaterialType, Workshop, ProductWorkshop
from forms import ProductForm, MaterialCalculatorForm
from services import calculate_production_time, calculate_raw_material
from config import Config
import os

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/products')
def products():
    all_products = Product.query.all()
    production_times = {}
    
    for product in all_products:
        production_times[product.id] = calculate_production_time(product.id)
    
    return render_template('products.html', 
                         products=all_products,
                         production_times=production_times)

@app.route('/product/add', methods=['GET', 'POST'])
def add_product():
    form = ProductForm()
    
    if form.validate_on_submit():
        try:
            # Проверяем, существует ли продукт с таким артикулом
            existing_product = Product.query.filter_by(article=form.article.data).first()
            if existing_product:
                flash('Продукт с таким артикулом уже существует!', 'error')
                return render_template('product_form.html', form=form)
            
            new_product = Product(
                article=form.article.data,
                product_type_id=form.product_type_id.data,
                name=form.name.data,
                description=form.description.data,
                min_cost_for_partner=form.min_cost_for_partner.data,
                main_material_id=form.main_material_id.data,
                parameter1=form.parameter1.data or 0,
                parameter2=form.parameter2.data or 0
            )
            
            db.session.add(new_product)
            db.session.commit()
            
            flash('Продукт успешно добавлен!', 'success')
            return redirect(url_for('products'))
        except Exception as e:
            db.session.rollback()
            print(f"Ошибка при добавлении продукта: {str(e)}")
            flash(f'Ошибка при добавлении продукта: {str(e)}', 'error')
    
    return render_template('product_form.html', form=form)

@app.route('/product/edit/<int:product_id>', methods=['GET', 'POST'])
def edit_product(product_id):
    product = Product.query.get_or_404(product_id)
    form = ProductForm(obj=product)
    
    if form.validate_on_submit():
        try:
            # Проверяем, не занят ли артикул другим продуктом
            existing_product = Product.query.filter(Product.article == form.article.data, Product.id != product_id).first()
            if existing_product:
                flash('Продукт с таким артикулом уже существует!', 'error')
                return render_template('product_form.html', form=form, product=product)
            
            product.article = form.article.data
            product.product_type_id = form.product_type_id.data
            product.name = form.name.data
            product.description = form.description.data
            product.min_cost_for_partner = form.min_cost_for_partner.data
            product.main_material_id = form.main_material_id.data
            product.parameter1 = form.parameter1.data or 0
            product.parameter2 = form.parameter2.data or 0
            
            db.session.commit()
            flash('Продукт успешно обновлен!', 'success')
            return redirect(url_for('products'))
        except Exception as e:
            db.session.rollback()
            print(f"Ошибка при обновлении продукта: {str(e)}")
            flash(f'Ошибка при обновлении продукта: {str(e)}', 'error')
    
    return render_template('product_form.html', form=form, product=product)

@app.route('/product/delete/<int:product_id>', methods=['POST'])
def delete_product(product_id):
    try:
        product = Product.query.get_or_404(product_id)
        
        # Сначала удаляем связанные записи в product_workshops
        ProductWorkshop.query.filter_by(product_id=product_id).delete()
        
        # Затем удаляем сам продукт
        db.session.delete(product)
        db.session.commit()
        
        flash('Продукт успешно удален!', 'success')
    except Exception as e:
        db.session.rollback()
        print(f"Ошибка при удалении продукта: {str(e)}")
        flash(f'Ошибка при удалении продукта: {str(e)}', 'error')
    
    return redirect(url_for('products'))

@app.route('/product/workshops/<int:product_id>')
def workshops(product_id):
    product = Product.query.get_or_404(product_id)
    product_workshops = ProductWorkshop.query.filter_by(product_id=product_id).all()
    total_time = calculate_production_time(product_id)
    
    return render_template('workshops.html', 
                         product=product, 
                         workshops=product_workshops,
                         total_time=total_time)

@app.route('/material-calculator', methods=['GET', 'POST'])
def material_calculator():
    form = MaterialCalculatorForm()
    result = None
    product_type = None
    material_type = None
    
    # Получаем типы продукции и материалов
    product_types = ProductType.query.all()
    material_types = MaterialType.query.all()
    
    if not product_types or not material_types:
        flash('Нет данных о типах продукции или материалах. Проверьте импорт данных.', 'error')
    
    if form.validate_on_submit():
        try:
            # Вычисляем результат
            result = calculate_raw_material(
                form.product_type_id.data,
                form.material_type_id.data,
                form.quantity.data,
                form.param1.data,
                form.param2.data
            )
            
            if result == -1:
                flash('Ошибка при расчете. Проверьте введенные данные.', 'error')
            else:
                product_type = ProductType.query.get(form.product_type_id.data)
                material_type = MaterialType.query.get(form.material_type_id.data)
                flash('Расчет успешно выполнен!', 'success')
        except Exception as e:
            print(f"Ошибка при расчете: {str(e)}")
            flash(f'Ошибка при расчете: {str(e)}', 'error')
    
    return render_template('material_calculator.html', 
                         form=form,
                         result=result,
                         product_type=product_type,
                         material_type=material_type,
                         product_types=product_types,
                         material_types=material_types)

if __name__ == '__main__':
    # Создаем папки для статики и шаблонов при первом запуске
    os.makedirs('static/css', exist_ok=True)
    os.makedirs('static/img', exist_ok=True)
    os.makedirs('static/js', exist_ok=True)
    os.makedirs('templates', exist_ok=True)
    
    # Создаем базу данных при первом запуске
    with app.app_context():
        db.create_all()
    
    app.run(debug=True)