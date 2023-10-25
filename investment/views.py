from rest_framework import generics, status
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.response import Response
from rest_framework.views import APIView
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Sum
from django.shortcuts import get_object_or_404

from . import serializers
from .models import Investment, InvestmentDocument, InvestingEntity
from .apps import InvestmentConfig as Conf
from utils.permissions import IsAdmin, IsInvestor, IsSponsor
from account.apps import AccountConfig
from account.models import CustomUser


# Investor: Commite Investment | All Active/completed Investments
# Sponsor:  Active Investments
class InvestmentListView(generics.ListCreateAPIView):
    permission_classes = (IsInvestor | IsSponsor,)
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter,)
    # search_fields = ['user__first_name', 'user__last_name', 'user__email', 'user__phone']

    def get_queryset(self):
        if self.request.user.user_type == AccountConfig.USER_INVESTOR:
            return Investment.objects.filter(
                deleted=False,
                status__in=[Conf.STATUS_ACTIVE, Conf.STATUS_COMPLETED]).order_by('-created_at')
        return Investment.objects.filter(
            deleted=False, status=Conf.STATUS_ACTIVE).order_by('-created_at')

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return serializers.InvestmentSerializer
        return serializers.InvestmentCreateSerializer


# Investor: Sign Opportunity Document
# Sponsor:  Add Report/Document To Investment
class InvestmentDetailView(generics.RetrieveUpdateAPIView):
    permission_classes = (IsInvestor | IsSponsor,)

    def get_queryset(self):
        if self.request.user.user_type == AccountConfig.USER_INVESTOR:
            return Investment.objects.filter(
                deleted=False, status__in=[Conf.STATUS_ACTIVE, Conf.STATUS_COMPLETED])
        return Investment.objects.filter(
            deleted=False, status=Conf.STATUS_ACTIVE)

    def get_serializer_class(self):
        if self.request.user.user_type == AccountConfig.USER_INVESTOR:
            return serializers.InvestmentSerializer

        if self.request.method == 'GET':
            return serializers.InvestmentSerializer
        return serializers.InvestmentDocumentSerializer


class InvestmentDocumentListView(generics.ListCreateAPIView):
    permission_classes = (IsInvestor | IsSponsor,)
    serializer_class = serializers.InvestmentDocumentSerializer

    def get_queryset(self):
        if self.request.user.user_type == AccountConfig.USER_INVESTOR:
            return InvestmentDocument.objects.filter(
                        deleted=False,
                        investment__status__in=[Conf.STATUS_ACTIVE, Conf.STATUS_COMPLETED],
                        investment=self.kwargs['pk']
                    ).order_by('-created_at')
        return InvestmentDocument.objects.filter(
                    deleted=False,
                    investment__status=Conf.STATUS_ACTIVE,
                    investment=self.kwargs['pk']
                ).order_by('-created_at')

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['pk'] = self.kwargs['pk']
        return context


class InvestmentDocumentDetailView(generics.RetrieveUpdateAPIView):
    permission_classes = (IsInvestor | IsSponsor,)
    serializer_class = serializers.InvestmentDocumentSerializer

    def get_queryset(self):
        if self.request.user.user_type == AccountConfig.USER_INVESTOR:
            return InvestmentDocument.objects.filter(
                        deleted=False,
                        investment__status__in=[Conf.STATUS_ACTIVE, Conf.STATUS_COMPLETED],
                        investment=self.kwargs['inv']
                    )
        return InvestmentDocument.objects.filter(
                    deleted=False,
                    investment__status=Conf.STATUS_ACTIVE,
                    investment=self.kwargs['inv']
                )


class ProfileInvestmentListView(generics.ListAPIView):
    permission_classes = (IsInvestor | IsSponsor,)
    serializer_class = serializers.InvestmentSerializer

    def get_queryset(self):
        if self.request.user.user_type == AccountConfig.USER_INVESTOR:
            return Investment.objects.filter(
                deleted=False, investing_entity__user=self.request.user).order_by('-created_at')
        return Investment.objects.filter(
            deleted=False, opportunity__sponspr=self.request.user.sponsor).order_by('-created_at')


class ProfileInvestmentDetailView(generics.RetrieveAPIView):
    permission_classes = (IsInvestor | IsSponsor,)
    serializer_class = serializers.InvestmentSerializer

    def get_queryset(self):
        if self.request.user.user_type == AccountConfig.USER_INVESTOR:
            return Investment.objects.filter(deleted=False, investing_entity__user=self.request.user)
        return Investment.objects.filter(deleted=False, opportunity__sponspr=self.request.user.sponsor)


class InvestmentEntitiesListView(generics.ListCreateAPIView):
    permission_classes = (IsInvestor,)
    pagination_class = None

    def get_queryset(self):
        return InvestingEntity.objects.filter(deleted=False, user=self.request.user).order_by('-created_at')

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return serializers.InvestingEntityListSerializer
        return serializers.InvestingEntitySerializer


class InvestmentEntitiesDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsInvestor,)
    serializer_class = serializers.InvestingEntitySerializer

    def get_queryset(self):
        return InvestingEntity.objects.filter(deleted=False, user=self.request.user)

    def perform_destroy(self, instance):
        instance.deleted = True
        instance.save()


# All Active/completed Investments |
class AdminInvestmentListView(generics.ListAPIView):
    permission_classes = (IsAdmin,)
    serializer_class = serializers.AdminInvestmentSerializer
    queryset = Investment.objects.filter(deleted=False).order_by('-created_at')
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
    ordering_fields = [
        'investing_entity__user__first_name',
        'investing_entity__user__last_name',
        'investing_entity__user__email',
        'investing_entity__user__phone',
        'opportunity__name',
        'amount',
    ]
    search_fields = [
        'investing_entity__user__first_name',
        'investing_entity__user__last_name',
        'investing_entity__user__email',
        'investing_entity__user__phone',
        'opportunity__name',
        'amount',
    ]
    filter_fields = ('status',)


# Promote Commited Investments | Add Doc | Toggle As Active/Completed Investment
class AdminInvestmentDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAdmin,)
    serializer_class = serializers.AdminInvestmentSerializer
    queryset = Investment.objects.filter(deleted=False)

    def perform_destroy(self, instance):
        instance.deleted = True
        instance.save()


class AdminInvestmentDocumentListView(generics.ListCreateAPIView):
    permission_classes = (IsAdmin,)
    serializer_class = serializers.InvestmentDocumentSerializer

    def get_queryset(self):
        return InvestmentDocument.objects.filter(
            deleted=False, investment=self.kwargs['pk']).order_by('-created_at')

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['pk'] = self.kwargs['pk']
        return context


class AdminInvestmentDocumentDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAdmin,)
    serializer_class = serializers.InvestmentDocumentSerializer

    def get_queryset(self):
        return InvestmentDocument.objects.filter(deleted=False, investment=self.kwargs['inv'])

    def perform_destroy(self, instance):
        instance.deleted = True
        instance.save()


class InvestorProfileOverviewView(APIView):
    permission_classes = (IsInvestor,)

    def get(self, request):
        overviews = {}

        user_investments = Investment.objects.filter(
            investing_entity__user=self.request.user,
            deleted=False,
            opportunity__deleted=False,
        )
        amount_funded = user_investments.aggregate(sum=Sum('amount'))['sum']
        value_increase = user_investments.aggregate(sum=Sum('opportunity__value_increase'))['sum']
        distribution_percentage = user_investments.aggregate(
            sum=Sum('opportunity__distribution_percentage')
        )['sum']

        if amount_funded:
            overviews['amount_funded'] = amount_funded
            overviews['marked_value'] = value_increase * amount_funded
            overviews['distribution'] = distribution_percentage * amount_funded
            overviews['sum_marked_value_distribution'] = (
                value_increase * amount_funded) + (distribution_percentage * amount_funded)
        else:
            overviews['amount_funded'] = 0
            overviews['marked_value'] = 0
            overviews['distribution'] = 0
            overviews['sum_marked_value_distribution'] = 0

        industries_dict = {}
        for invest in user_investments:
            for industry in invest.opportunity.industries.filter(deleted=False):
                if industries_dict.get(industry.title):
                    industries_dict[industry.title] = industries_dict[industry.title] + invest.amount
                else:
                    industries_dict[industry.title] = invest.amount

        industries = []
        for item in industries_dict:
            industries.append({
                'title': item,
                'amount': industries_dict[item],
            })

        return Response(
                    {
                        'overviews': overviews,
                        'asset_types': industries,
                    },
                    status=status.HTTP_200_OK
                )


class AdminInvestmentEntitiesListView(generics.ListCreateAPIView):
    permission_classes = (IsAdmin,)
    pagination_class = None

    def get_queryset(self):
        user = get_object_or_404(CustomUser.objects.filter(deleted=False), id=self.kwargs['pk'])
        return InvestingEntity.objects.filter(deleted=False, user=user)

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return serializers.InvestingEntityListSerializer
        return serializers.InvestingEntitySerializer


class AdminInvestorProfileOverviewView(APIView):
    permission_classes = (IsAdmin,)

    def get(self, request, pk):
        overviews = {}

        user = get_object_or_404(CustomUser.objects.filter(deleted=False), id=pk)

        user_investments = Investment.objects.filter(investing_entity__user=user, deleted=False)
        amount_funded = user_investments.aggregate(sum=Sum('amount'))['sum']
        value_increase = user_investments.aggregate(sum=Sum('opportunity__value_increase'))['sum']
        distribution_percentage = user_investments.aggregate(
            sum=Sum('opportunity__distribution_percentage')
        )['sum']

        if amount_funded:
            overviews['amount_funded'] = amount_funded
            overviews['marked_value'] = value_increase * amount_funded
            overviews['distribution'] = distribution_percentage * amount_funded
            overviews['sum_marked_value_distribution'] = (
                value_increase * amount_funded) + (distribution_percentage * amount_funded)
        else:
            overviews['amount_funded'] = 0
            overviews['marked_value'] = 0
            overviews['distribution'] = 0
            overviews['sum_marked_value_distribution'] = 0

        industries_dict = {}
        for invest in user_investments:
            for industry in invest.opportunity.industries.filter(deleted=False):
                if industries_dict.get(industry.title):
                    industries_dict[industry.title] = industries_dict[industry.title] + invest.amount
                else:
                    industries_dict[industry.title] = invest.amount

        industries = []
        for item in industries_dict:
            industries.append({
                'title': item,
                'amount': industries_dict[item],
            })

        return Response(
                    {
                        'overviews': overviews,
                        'asset_types': industries,
                    },
                    status=status.HTTP_200_OK
                )


# class PDFGENView(APIView):
#     def get(self, request):
#         from utils.pdf_gen import pdf_gen
#         return Response(
#                     {
#                         'result': pdf_gen(),
#                     },
#                     status=status.HTTP_200_OK
#                 )
