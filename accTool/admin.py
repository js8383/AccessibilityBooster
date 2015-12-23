from django.contrib import admin
from accTool.models import UserProfile
from accTool.models import Document,ParsedImage,Headings,Metadata

# Register your models here.
admin.site.register(UserProfile)
admin.site.register(Document)
admin.site.register(ParsedImage)
admin.site.register(Headings)
admin.site.register(Metadata)



