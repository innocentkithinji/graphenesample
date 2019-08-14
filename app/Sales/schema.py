from .models import Sale
import graphene
from graphene_django import DjangoObjectType
from Farm.models import Farm
from Products.models import Product
from Units.models import Unit
from County.models import County


class SaleType(DjangoObjectType):
    class Meta:
        model = Sale


class Query(graphene.ObjectType):
    sales = graphene.List(SaleType)

    def resolve_sales(self, info):
        return Sale.objects.all()


class CreateSale(graphene.Mutation):
    sale = graphene.Field(SaleType)

    class Arguments:
        farm_id = graphene.Int(required=True)
        product_id = graphene.Int(required=True)
        unit_id = graphene.Int(required=True)
        amount = graphene.Float(required=True)
        county_id = graphene.Int(required=True)
        price = graphene.Float(required=True)

    def mutate(self, info, farm_id, product_id, unit_id, amount, county_id, price):
        farm = Farm.objects.get(id=farm_id)
        product = Product.objects.get(id=product_id)
        unit = Unit.objects.get(id=unit_id)
        county = County.objects.get(id=county_id)

        sale = Sale(farm=farm, product=product, amount=amount, unit=unit, county=county, price=price)
        sale.save()

        return CreateSale(sale=sale)


class UpdateSale(graphene.Mutation):
    sale = graphene.Field(SaleType)

    class Arguments:
        sale_id = graphene.Int(required=True)
        product_id = graphene.Int()
        unit_id = graphene.Int()
        amount = graphene.Float()
        price = graphene.Float()

    def mutate(self, info, farm_id, product_id, unit_id, amount, sale_id, price):
        sale = Sale.object.get(id=sale_id)
        farm = Farm.objects.get(id=farm_id)
        product = Product.objects.get(id=product_id)
        unit = Unit.objects.get(id=unit_id)

        sale.farm = farm
        sale.product = product
        sale.unit = unit
        sale.amount = amount
        sale.price = price

        sale.save()

        return UpdateSale(sale=sale)


class Mutation(graphene.ObjectType):
    create_sale = CreateSale.Field()
    update_sale = UpdateSale.Field()
