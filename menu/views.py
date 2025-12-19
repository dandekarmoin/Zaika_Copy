from django.shortcuts import render

# def menu_list(request):
#     starters = [
#         ('Paneer Tikka', 'Grilled cottage cheese marinated in spices', 180),
#         ('Chicken Tandoori', 'Classic clay-oven roasted chicken (half portion)', 250),
#         ('Hara Bhara Kabab', 'Healthy pan-fried green vegetable cutlets', 160),
#         ('Crispy Chicken', 'Deep-fried chicken strips tossed in schezwan sauce', 190),
#         ('Veg Manchurian', 'Indo-Chinese fried vegetable balls in gravy', 150),
#         ('Chilli Paneer (Dry)', 'Wok-tossed paneer with capsicum and onions', 210),
#         ('Fish Amritsari', 'Crispy spiced fish fillets', 280),
#         ('Soya Chaap Tikka', 'Marinated roasted soya chaap pieces', 190),
#     ]

#     main_course = [
#         ('Butter Chicken', 'Smoky chicken pieces in a creamy tomato gravy', 320),
#         ('Chicken Curry', 'Traditional North Indian chicken curry (home style)', 280),
#         ('Paneer Butter Masala', 'Rich & creamy paneer cubes in tomato gravy', 260),
#         ('Dal Tadka', 'Classic yellow lentil curry tempered with ghee and spices', 150),
#         ('Chole Masala', 'Spicy chickpea curry', 140),
#         ('Rajma Masala', 'Kidney beans cooked in thick, spicy gravy', 160),
#         ('Shahi Paneer', 'Paneer in a thick, sweet, and creamy cashew gravy', 270),
#         ('Mutton Rogan Josh', 'Kashmiri style mutton curry with rich spices', 380),
#         ('Palak Paneer', 'Paneer cubes in a creamy spinach gravy', 250),
#     ]

#     biryani = [
#         ('Veg Biryani', 'Aromatic basmati rice layered with mixed vegetables', 200),
#         ('Chicken Biryani', 'Spicy dum cooked chicken and rice', 280),
#         ('Mutton Biryani', 'Rich long-grain rice with tender mutton pieces', 350),
#         ('Hyderabadi Biryani', 'Authentic style spicy biryani', 300),
#         ('Egg Biryani', 'Layered rice with boiled eggs and spices', 220),
#     ]

#     breads = [
#         ('Butter Naan', 'Soft & buttery Indian flatbread', 40),
#         ('Tandoori Roti', 'Whole wheat flatbread baked in clay oven', 20),
#         ('Garlic Naan', 'Naan flavored with chopped garlic and coriander', 60),
#         ('Lachha Paratha', 'Layered crispy whole wheat paratha', 45),
#         ('Missi Roti', 'Flatbread made with gram flour and wheat flour', 35),
#         ('Aloo Paratha', 'Whole wheat bread stuffed with spiced potatoes', 70),
#     ]

#     rice_and_noodles = [
#         ('Jeera Rice', 'Basmati rice tempered with cumin seeds', 120),
#         ('Steamed Rice', 'Plain boiled basmati rice', 90),
#         ('Veg Fried Rice', 'Chinese style rice tossed with vegetables', 160),
#         ('Chicken Fried Rice', 'Chinese style rice tossed with chicken', 190),
#         ('Hakka Noodles (Veg)', 'Wok-tossed noodles with shredded vegetables', 170),
#     ]

#     snacks = [
#         ('Samosa (2 pcs)', 'Crispy fried pastry filled with spiced potato', 40),
#         ('Kachori (2 pcs)', 'Spicy stuffed kachori', 50),
#         ('French Fries', 'Crispy potato fries', 70),
#         ('Veg Sandwich (Grilled)', 'Loaded grilled vegetable sandwich', 90),
#         ('Chicken Sandwich (Grilled)', 'Grilled chicken and cheese sandwich', 120),
#         ('Vada Pav', 'Maharashtrian street food staple', 30),
#     ]

#     beverages = [
#         ('Masala Chai', 'Spiced Indian tea with milk', 20),
#         ('Cold Coffee', 'Iced creamy coffee', 80),
#         ('Fresh Lime Soda', 'Sweet & salty lemon soda', 50),
#         ('Lassi (Sweet/Salted)', 'Thick, sweet/salty Punjabi yogurt drink', 60),
#         ('Thandai', 'Traditional festive almond and spice drink', 70),
#         ('Bottled Water (1L)', 'Mineral water bottle', 30),
#     ]

#     desserts = [
#         ('Gulab Jamun (2 pcs)', 'Sweet deep-fried milk dumplings in sugar syrup', 60),
#         ('Rasgulla (2 pcs)', 'Soft spongy cottage cheese sweets', 50),
#         ('Kheer', 'Traditional Indian rice pudding dessert', 70),
#         ('Ice Cream (Scoop)', 'Vanilla/Strawberry/Chocolate frozen dessert', 80),
#         ('Gajar Halwa', 'Warm carrot dessert cooked in ghee and milk', 110),
#     ]

#     context = {
#         'starters': starters,
#         'main_course': main_course,
#         'biryani': biryani,
#         'breads': breads,
#         'rice_and_noodles': rice_and_noodles,
#         'snacks': snacks,
#         'beverages': beverages,
#         'desserts': desserts,
#     }

#     return render(request, 'main/menu_list.html', context)

from cart.models import MenuItem

def menu_list(request):
    context = {
        'starters': MenuItem.objects.filter(category='starters'),
        'main_course': MenuItem.objects.filter(category='main_course'),
        'biryani': MenuItem.objects.filter(category='biryani'),
        'breads': MenuItem.objects.filter(category='breads'),
        'rice_and_noodles': MenuItem.objects.filter(category='rice'),
        'snacks': MenuItem.objects.filter(category='snacks'),
        'beverages': MenuItem.objects.filter(category='beverages'),
        'desserts': MenuItem.objects.filter(category='desserts'),
    }

    # Choose a featured menu item (prefer items with images) from categories shown on the page
    visible_categories = ['starters', 'main_course', 'biryani']
    featured = MenuItem.objects.filter(category__in=visible_categories, image__isnull=False).order_by('?').first()
    if not featured:
        # fallback to any menu item with an image
        featured = MenuItem.objects.filter(image__isnull=False).order_by('?').first()
    context['featured'] = featured

    # Load a few recent customer reviews to display below the menu (show up to 6)
    from main.models import Review
    reviews_list = Review.objects.all()[:6]
    context['reviews_list'] = reviews_list

    return render(request, 'main/menu_list.html', context)


def menu_3d(request):
    """Render a simple 3D gallery where each menu item is represented
    as a textured 3D card built from the item's image."""
    items = MenuItem.objects.all()
    return render(request, 'menu/3d_gallery.html', {'items': items})
