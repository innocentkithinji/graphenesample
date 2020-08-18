import graphene
from Agent.schema import Query as AgentQuery, Mutation as AgentMutation
from Buyer.schema import Mutation as BuyerMutation
from Buyer.schema import Query as BuyerQuery
from Categories.schema import Query as CategoryQuery
from Chats.schema import Query as ChatQuery, Mutation as ChatMutation
from Country.schema import Query as CountryQuery
from County.schema import Query as CountyQuery
from Farm.schema import Query as FarmQuery, Mutation as FarmMutation
from Labour.schema import Query as LabourQuery, Mutation as LabourSMutation
from LabourApplications.schema import Query as LabourApplicationQuery, Mutation as LabourApplicationMutation
from Labourers.schema import Query as LabourerQuery, Mutation as LabourerMutation
from Members.schema import Query as MembersQuery, Mutation as MemberMutation
from Mpesa.schema import Mutation as MpesaMutation
from Packages.schema import Query as PackagesQuery
from Products.schema import Query as ProductsQuery
from Sales.schema import Query as SalesQuery, Mutation as SaleMutation
from Tenders.schema import Query as TenderQuery, Mutation as TenderMutation
from Units.schema import Query as UnitsQuery
from Wards.schema import Query as WardsQuery


class Query(CountyQuery, CountryQuery, MembersQuery, BuyerQuery, CategoryQuery, TenderQuery, FarmQuery, PackagesQuery,
            ProductsQuery, LabourQuery, SalesQuery, UnitsQuery, WardsQuery, ChatQuery, AgentQuery, LabourerQuery,
            LabourApplicationQuery, graphene.ObjectType):
    pass


class Mutation(MemberMutation, FarmMutation, TenderMutation, BuyerMutation, SaleMutation, ChatMutation, AgentMutation,
               LabourSMutation, LabourerMutation, MpesaMutation, LabourApplicationMutation, graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)
