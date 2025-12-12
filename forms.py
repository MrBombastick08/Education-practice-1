from flask_wtf import FlaskForm
from wtforms import StringField, DecimalField, IntegerField, SelectField, TextAreaField
from wtforms.validators import DataRequired, NumberRange, ValidationError
from models import ProductType, MaterialType, db

def validate_positive(form, field):
    if field.data is not None and field.data <= 0:
        raise ValidationError('Значение должно быть положительным')

def validate_decimal(form, field):
    if field.data <= 0:
        raise ValidationError('Значение должно быть положительным числом')

class ProductForm(FlaskForm):
    article = StringField('Артикул', validators=[DataRequired()])
    product_type_id = SelectField('Тип продукции', coerce=int, validators=[DataRequired()])
    name = StringField('Наименование', validators=[DataRequired()])
    description = TextAreaField('Описание')
    min_cost_for_partner = DecimalField('Минимальная стоимость для партнера', 
                                        validators=[DataRequired(), NumberRange(min=0)])
    main_material_id = SelectField('Основной материал', coerce=int, validators=[DataRequired()])
    parameter1 = DecimalField('Параметр 1 (размер/площадь)', validators=[validate_positive])
    parameter2 = DecimalField('Параметр 2 (другой размер)', validators=[validate_positive])
    
    def __init__(self, *args, **kwargs):
        super(ProductForm, self).__init__(*args, **kwargs)
        self.product_type_id.choices = [(pt.id, pt.name) for pt in ProductType.query.all()]
        self.main_material_id.choices = [(mt.id, mt.name) for mt in MaterialType.query.all()]

class MaterialCalculatorForm(FlaskForm):
    product_type_id = SelectField('Тип продукции', coerce=int, validators=[DataRequired()])
    material_type_id = SelectField('Тип материала', coerce=int, validators=[DataRequired()])
    quantity = IntegerField('Количество продукции', validators=[DataRequired(), NumberRange(min=1)])
    param1 = DecimalField('Параметр 1', validators=[DataRequired(), validate_decimal])
    param2 = DecimalField('Параметр 2', validators=[DataRequired(), validate_decimal])
    
    def __init__(self, *args, **kwargs):
        super(MaterialCalculatorForm, self).__init__(*args, **kwargs)
        self.product_type_id.choices = [(pt.id, pt.name) for pt in ProductType.query.order_by(ProductType.name).all()]
        self.material_type_id.choices = [(mt.id, mt.name) for mt in MaterialType.query.order_by(MaterialType.name).all()]