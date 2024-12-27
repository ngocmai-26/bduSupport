from rest_framework import serializers

from bduSuport.models.backoffice_autdit_log import BackofficeAuditLog


class BackofficeAuditLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = BackofficeAuditLog
        fields = "__all__"

    email = serializers.SerializerMethodField()

    def get_email(self, obj: BackofficeAuditLog):
        return obj.user.email