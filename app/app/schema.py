import graphene
from Country.schema import Query as CountryQuery
from County.schema import Query as CountyQuery
from Members.schema import Query as MembersQuery, Mutation as MemberMutation
from Buyer.schema import Query as BuyerQuery
from Buyer.schema import Mutation as BuyerMutation
from Categories.schema import Query as CategoryQuery
from Farm.schema import Query as FarmQuery, Mutation as FarmMutation
from Packages.schema import Query as PackagesQuery
from Products.schema import Query as ProductsQuery
from Sales.schema import Query as SalesQuery, Mutation as SaleMutation
from Units.schema import Query as UnitsQuery
from Tenders.schema import Query as TenderQuery


class Query(CountyQuery, CountryQuery, MembersQuery, BuyerQuery, CategoryQuery, TenderQuery, FarmQuery, PackagesQuery, ProductsQuery,
            SalesQuery, UnitsQuery, graphene.ObjectType):
    pass


class Mutation(MemberMutation, FarmMutation, BuyerMutation, SaleMutation, graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)