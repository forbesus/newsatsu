from django.contrib import admin

from .models import (
    BidModel,
    ConstructionModel,
    HearingModel,
    HireModel,
    RequestAnswerModel,
    RequestCompanyModel,
    RequestQuestionModel,
)

admin.site.register(ConstructionModel)
admin.site.register(RequestCompanyModel)
admin.site.register(RequestAnswerModel)
admin.site.register(RequestQuestionModel)
admin.site.register(HireModel)
admin.site.register(HearingModel)
admin.site.register(BidModel)
