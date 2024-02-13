from django.contrib import admin
from merchapp.models import products, cart, userextrainfo, wishlist,history,ContactPage
# Register your models here.
class adminProd(admin.ModelAdmin):
    list_display=['id','pname','pbrand','category','price', 'discount','disprice', 'image', 'totalsells']
    list_filter=['pbrand']

admin.site.register(products,adminProd)

class cartView(admin.ModelAdmin):
    list_display=['id','pid','uid', 'quantity']
admin.site.register(cart,cartView)

class historyView(admin.ModelAdmin):
    list_display=['id','pid','uid', 'quantity']
admin.site.register(history,historyView)

class extrainfoView(admin.ModelAdmin):
    list_display=['id','uid','address','phonenum', 'profilepic']
admin.site.register(userextrainfo, extrainfoView)

class wishlistView(admin.ModelAdmin):
    list_display=['id','pid','uid']
admin.site.register(wishlist, wishlistView)

class contactpageView(admin.ModelAdmin):
    list_display=['id','uid','messege']
admin.site.register(ContactPage, contactpageView)