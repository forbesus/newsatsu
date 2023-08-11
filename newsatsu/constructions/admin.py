from django.contrib import admin

from .models import ConstructionModel, RequestAnswer, RequestCompanyModel, RequestQuestion

admin.site.register(ConstructionModel)
admin.site.register(RequestCompanyModel)
admin.site.register(RequestAnswer)
admin.site.register(RequestQuestion)
