from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from . import models
from account.serializers import UserProfileSerializer
from opportunity.serializers import CountrySerializer, OpportunitySerializer, OpportunityDocumentSerializer
from opportunity.models import Country
from opportunity.apps import OpportunityConfig


class AccountIndividualSerializer(serializers.ModelSerializer):
    citizenship_info = CountrySerializer(source='citizenship', read_only=True)

    class Meta:
        model = models.AccountIndividual
        fields = (
            'id',
            'birthday',
            'citizenship',
            'citizenship_info',
            'tax_id',
        )


class AccountEntitySerializer(serializers.ModelSerializer):
    country_info = CountrySerializer(source='country', read_only=True)

    class Meta:
        model = models.AccountEntity
        fields = (
            'id',
            'company',
            'tax_id',
            'country',
            'country_info',
            'state',
            'questionnaire',
        )


class InvestingEntityListSerializer(serializers.ModelSerializer):
    user = UserProfileSerializer()
    account_type_info = serializers.SerializerMethodField(read_only=True)
    account_individual_info = AccountIndividualSerializer(source='account_individual', read_only=True)
    account_entity_info = AccountEntitySerializer(source='account_entity', read_only=True)

    class Meta:
        model = models.InvestingEntity
        fields = (
            'id',
            'user',
            'account_type_info',
            'account_individual',
            'account_individual_info',
            'account_entity',
            'account_entity_info',
        )

    def get_account_type_info(self, obj):
        if obj.account_individual:
            return "Individual Account"
        return "Entity Account"


class InvestingEntitySerializer(serializers.ModelSerializer):
    user = UserProfileSerializer()
    account_individual_info = AccountIndividualSerializer(source='account_individual', read_only=True)
    account_entity_info = AccountEntitySerializer(source='account_entity', read_only=True)
    banks_info = serializers.SerializerMethodField(read_only=True)
    addresses_info = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = models.InvestingEntity
        fields = (
            'id',
            'user',
            'account_individual',
            'account_individual_info',
            'account_entity',
            'account_entity_info',
            'questionnaire',
            'has_future_credit_account',
            'has_intermediary_account',
            'banks_info',
            'addresses_info',
        )

    def get_banks_info(self, obj):
        if obj.bank_investment.filter(deleted=False).exists():
            return BankAccountSerializer(obj.bank_investment.filter(deleted=False), many=True).data
        return None

    def get_addresses_info(self, obj):
        if obj.address_investment.filter(deleted=False).exists():
            return AddressSerializer(obj.address_investment.filter(deleted=False), many=True).data
        return None


class InvestmentDocumentSerializer(serializers.ModelSerializer):
    opportunity_document_info = OpportunityDocumentSerializer(source='opportunity_document', read_only=True)
    type_info = serializers.CharField(source='get_type_display', read_only=True)

    class Meta:
        model = models.InvestmentDocument
        fields = (
            'id',
            'title',
            'opportunity_document',
            'opportunity_document_info',
            'file',
            'signature',
            'signature_date',
            'description',
            'type',
            'type_info',
        )

    def create(self, validated_data):
        validated_data['investment_id'] = self.context.get('pk')
        return models.InvestmentDocument.objects.create(**validated_data)


class SubscriptionDocumentsSerializer(serializers.Serializer):
    file = serializers.FileField()


class BaseInvestmentSerializer(serializers.ModelSerializer):
    investing_entity_info = InvestingEntitySerializer(source='investing_entity', read_only=True)
    opportunity_info = OpportunitySerializer(source='opportunity', read_only=True)
    status_info = serializers.CharField(source='get_status_display', read_only=True)
    documents_info = serializers.SerializerMethodField(read_only=True)
    subscription_documents = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = models.Investment
        fields = (
            'id',
            'investing_entity',
            'investing_entity_info',
            'opportunity',
            'opportunity_info',
            'amount',
            'status',
            'status_info',
            'description',
            'price_per_share',
            'documents_info',
            'subscription_documents',
        )
        read_only_fields = ('status',)

    def get_documents_info(self, obj):
        if obj.document.filter(deleted=False).exists():
            return InvestmentDocumentSerializer(obj.document.filter(deleted=False), many=True).data
        return None

    def get_subscription_documents(self, obj):
        if obj.opportunity.document.filter(type=OpportunityConfig.TYPE_PDF).exists():
            return SubscriptionDocumentsSerializer(
                        obj.opportunity.document.filter(type=OpportunityConfig.TYPE_PDF),
                        context={'request': self.context['request']},
                        many=True,
                    ).data
        return []


class InvestmentSerializer(BaseInvestmentSerializer):
    class Meta:
        model = models.Investment
        fields = BaseInvestmentSerializer.Meta.fields
        read_only_fields = ('status',)


class AdminInvestmentSerializer(BaseInvestmentSerializer):
    class Meta:
        model = models.Investment
        fields = BaseInvestmentSerializer.Meta.fields


class QuestionValidatorSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    answer = serializers.BooleanField(required=False, allow_null=True)
    answer_desc = serializers.CharField(required=False, allow_null=True, allow_blank=True)


class InvestmentCreateSerializer(serializers.Serializer):
    opportunity_id = serializers.IntegerField(write_only=True)
    amount = serializers.IntegerField(
        write_only=True, required=False, allow_null=True)
    description = serializers.CharField(
        write_only=True, required=False, allow_null=True, allow_blank=True)
    electronic_notice = serializers.BooleanField(
        write_only=True, required=False, allow_null=True)
    signature_text = serializers.CharField(
        write_only=True, required=False, allow_null=True, allow_blank=True)

    investor_ent_id = serializers.IntegerField(
        write_only=True, required=False, allow_null=True)
    investor_type = serializers.CharField(
        write_only=True, required=False, allow_null=True, allow_blank=True)

    acc_ind_birthday = serializers.DateField(
        write_only=True, required=False, allow_null=True)
    acc_ind_citizenship_title = serializers.CharField(
        write_only=True, required=False, allow_null=True, allow_blank=True)
    acc_ind_tax_id = serializers.CharField(
        write_only=True, required=False, allow_null=True, allow_blank=True)

    acc_ent_company = serializers.CharField(
        write_only=True, required=False, allow_null=True, allow_blank=True)
    acc_ent_tax_id = serializers.CharField(
        write_only=True, required=False, allow_null=True, allow_blank=True)
    acc_ent_country_title = serializers.CharField(
        write_only=True, required=False, allow_null=True, allow_blank=True)
    acc_ent_state = serializers.CharField(
        write_only=True, required=False, allow_null=True, allow_blank=True)
    acc_ent_questionnaire = serializers.JSONField(
        write_only=True, required=False, allow_null=True)

    inv_ent_questionnaire = serializers.JSONField(
        write_only=True, required=False, allow_null=True)
    inv_ent_has_future_credit_account = serializers.BooleanField(
        write_only=True, required=False, allow_null=True)
    inv_ent_has_intermediary_account = serializers.BooleanField(
        write_only=True, required=False, allow_null=True)

    bnk_account_type = serializers.IntegerField(
        write_only=True, required=False, allow_null=True)
    bnk_country_title = serializers.CharField(
        write_only=True, required=False, allow_null=True, allow_blank=True)
    bnk_name = serializers.CharField(
        write_only=True, required=False, allow_null=True, allow_blank=True)
    bnk_wire = serializers.CharField(
        write_only=True, required=False, allow_null=True, allow_blank=True)
    bnk_account_name = serializers.CharField(
        write_only=True, required=False, allow_null=True, allow_blank=True)
    bnk_account_number = serializers.CharField(
        write_only=True, required=False, allow_null=True, allow_blank=True)

    add_country_title = serializers.CharField(
        write_only=True, required=False, allow_null=True, allow_blank=True)
    add_street1 = serializers.CharField(
        write_only=True, required=False, allow_null=True, allow_blank=True)
    add_street2 = serializers.CharField(
        write_only=True, required=False, allow_null=True, allow_blank=True)
    add_city = serializers.CharField(
        write_only=True, required=False, allow_null=True, allow_blank=True)
    add_state = serializers.CharField(
        write_only=True, required=False, allow_null=True, allow_blank=True)
    add_zipcode = serializers.CharField(
        write_only=True, required=False, allow_null=True, allow_blank=True)

    def validate_investor_type(self, attr):
        if attr not in ['individual', 'entity']:
            raise ValidationError("Value Choices: individual | entity")
        return attr

    def validate_acc_ent_questionnaire(self, attr):
        if attr:
            for item in attr:
                serializer = QuestionValidatorSerializer(data=item)
                serializer.is_valid(raise_exception=True)
        return attr

    def validate_inv_ent_questionnaire(self, attr):
        if attr:
            for item in attr:
                serializer = QuestionValidatorSerializer(data=item)
                serializer.is_valid(raise_exception=True)
        return attr

    def create(self, data):
        acc_ind = None
        acc_ent = None
        if data.get('investor_ent_id'):
            try:
                inv_ent = models.InvestingEntity.objects.get(id=data.get('investor_ent_id'))
            except:
                raise ValidationError("Investment Entity ID Does Not Exist.")
        else:
            if data.get('investor_type') == 'individual':
                country, _ = Country.objects.get_or_create(title=data.get('acc_ind_citizenship_title'))
                acc_ind = models.AccountIndividual.objects.create(
                                birthday=data.get('acc_ind_birthday'),
                                citizenship=country,
                                tax_id=data.get('acc_ind_tax_id'),
                            )
            else:
                country, _ = Country.objects.get_or_create(title=data.get('acc_ent_country_title'))
                acc_ent = models.AccountEntity.objects.create(
                                company=data.get('acc_ent_company'),
                                tax_id=data.get('acc_ent_tax_id'),
                                country=country,
                                state=data.get('acc_ent_state'),
                                questionnaire=data.get('acc_ent_questionnaire'),
                            )
            inv_ent = models.InvestingEntity.objects.create(
                            user=self.context['request'].user,
                            account_individual=acc_ind,
                            account_entity=acc_ent,
                            questionnaire=data.get('inv_ent_questionnaire'),
                            has_future_credit_account=data.get('inv_ent_has_future_credit_account', False),
                            has_intermediary_account=data.get('inv_ent_has_intermediary_account', False),
                        )

            bnk_country, _ = Country.objects.get_or_create(title=data.get('bnk_country_title'))
            models.BankAccount.objects.create(
                investing_entity=inv_ent,
                account_type=data.get('bnk_account_type'),
                country=bnk_country,
                name=data.get('bnk_name'),
                wire=data.get('bnk_wire'),
                account_name=data.get('bnk_account_name'),
                account_number=data.get('bnk_account_number'),
            )

            add_country, _ = Country.objects.get_or_create(title=data.get('add_country_title'))
            models.Address.objects.create(
                investing_entity=inv_ent,
                country=add_country,
                street1=data.get('add_street1'),
                street2=data.get('add_street2'),
                city=data.get('add_city'),
                state=data.get('add_state'),
                zipcode=data.get('add_zipcode'),
            )

        instance = models.Investment.objects.create(
                    investing_entity=inv_ent,
                    opportunity_id=data.get('opportunity_id'),
                    amount=data.get('amount'),
                    description=data.get('description'),
                    electronic_notice=data.get('electronic_notice', False),
                    signature_text=data.get('signature_text', None),
                )
        return instance

    def to_representation(self, value):
        return InvestmentSerializer(value, context={'request': self.context['request']}).data


class BankAccountSerializer(serializers.ModelSerializer):
    account_type_info = serializers.CharField(source='get_account_type_display', read_only=True)
    country_info = CountrySerializer(source='country', read_only=True)

    class Meta:
        model = models.BankAccount
        fields = (
            'id',
            'account_type',
            'account_type_info',
            'country',
            'country_info',
            'name',
            'wire',
            'account_name',
            'account_number',
        )


class AddressSerializer(serializers.ModelSerializer):
    country_info = CountrySerializer(source='country', read_only=True)

    class Meta:
        model = models.Address
        fields = (
            'id',
            'country',
            'country_info',
            'street1',
            'street2',
            'city',
            'state',
            'zipcode',
        )
