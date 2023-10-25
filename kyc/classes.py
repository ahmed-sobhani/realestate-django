import time
import onfido
from django.conf import settings
from rest_framework.exceptions import ValidationError

from .models import KYCFile
from .apps import KycConfig as Config
from account.serializers import AccreditationUserSerializer
from account.models import CustomUser


class KYC:
    def __init__(self):
        self.api = onfido.Api(settings.ONFIDO_TOKEN)

    def applicant(self, user: CustomUser):
        serializer = AccreditationUserSerializer(user).data
        try:
            applicant = self.api.applicant.create(serializer)
            return applicant['id']
        except Exception as error:
            raise ValidationError({
                'error': 'Something went wrong with Onfido.',
                'message': str(error),
            })

    def document(self, applicant_id, file):
        request_body = {"applicant_id": applicant_id, "type": "passport"}
        sample_file = open(file.path, "rb")
        self.api.document.upload(sample_file, request_body)

    def photo(self, applicant_id, file):
        request_body = {"applicant_id": applicant_id}
        sample_file = open(file.path, "rb")
        self.api.live_photo.upload(sample_file, request_body)

    def check(self, applicant_id):
        request_body = {"applicant_id": applicant_id, "report_names": ["document", "facial_similarity_photo"]}
        check = self.api.check.create(request_body)
        return check['report_ids']

    def report(self, report_id):
        return self.api.report.find(report_id)['status']

    def user_validation(self, user):
        applicant_id = self.applicant(user)
        for doc in KYCFile.objects.filter(investor__user=user):
            if doc.file_type == Config.PASSPORT:
                try:
                    self.document(applicant_id, doc.file)
                except:
                    return 'Onfido Validation Error: Passport.'
            if doc.file_type == Config.PHOTO:
                try:
                    self.photo(applicant_id, doc.file)
                except:
                    return 'Onfido Validation Error: Selfie.'

        report_ids = self.check(applicant_id)

        time.sleep(5)
        response = 'Completed.'
        for report_id in list(report_ids):
            if self.report(report_id) != 'complete':
                response = 'Failed!'
                break
        return response

    # def webhook(self):
    #     request_body = {
    #         "url": "https://<URL>",
    #         "events": [
    #                 "report.completed",
    #                 "check.completed"
    #             ]
    #     }

    #     api.webhook.create(request_body)    # => Registers a webhook
    #     api.webhook.find("<WEBHOOK_ID>")    # => Finds a single webhook
    #     api.webhook.edit("<WEBHOOK_ID>", new_webhook_details)   # => Edits a webhook
    #     api.webhook.delete("<WEBHOOK_ID>")  # => Deletes a webhook
    #     api.webhook.all()   # => Returns all webhooks
