from django.contrib import admin

from .models import BidModel, ConstructionModel, HearingModel, HireModel, RequestCompanyModel, RequestQAModel

admin.site.register(ConstructionModel)
admin.site.register(RequestCompanyModel)
admin.site.register(RequestQAModel)
admin.site.register(HireModel)
admin.site.register(HearingModel)
admin.site.register(BidModel)
