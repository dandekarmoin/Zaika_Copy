from cart.models import MenuItem

MENU_ITEMS = [
    # -------- Starters --------
    ("Paneer Tikka", "Grilled cottage cheese marinated in spices", 180, "paneer_tikka.png"),
    ("Chicken Tandoori", "Classic clay-oven roasted chicken (half portion)", 250, "chicken_tandoori.png"),
    ("Hara Bhara Kabab", "Healthy pan-fried green vegetable cutlets", 160, "hara_bhara_kabab.png"),
    ("Crispy Chicken", "Deep-fried chicken strips tossed in schezwan sauce", 190, "crispy_chicken.jpg"),
    ("Veg Manchurian", "Indo-Chinese fried vegetable balls in gravy", 150, "veg_manchurian.jpg"),
    ("Chilli Paneer (Dry)", "Wok-tossed paneer with capsicum and onions", 210, "chilli_paneer_dry.png"),
    ("Fish Amritsari", "Crispy spiced fish fillets", 280, "fish_amritsari.png"),
    ("Soya Chaap Tikka", "Marinated roasted soya chaap pieces", 190, "soya_chaap_tikka.png"),

    # -------- Main Course --------
    ("Butter Chicken", "Smoky chicken pieces in a creamy tomato gravy", 320, "butter_chicken.png"),
    ("Chicken Curry", "Traditional North Indian chicken curry (home style)", 280, "chicken_curry.png"),
    ("Paneer Butter Masala", "Rich & creamy paneer cubes in tomato gravy", 260, "paneer_butter_masala.png"),
    ("Dal Tadka", "Classic yellow lentil curry tempered with ghee and spices", 150, "dal_tadka.png"),
    ("Chole Masala", "Spicy chickpea curry", 140, "chole_masala.png"),
    ("Rajma Masala", "Kidney beans cooked in thick, spicy gravy", 160, "rajma_chawal.png"),
    ("Shahi Paneer", "Paneer in a thick, sweet, and creamy cashew gravy", 270, "shahi_paneer.png"),
    ("Mutton Rogan Josh", "Kashmiri style mutton curry with rich spices", 380, "mutton_rogan_josh.png"),
    ("Palak Paneer", "Paneer cubes in a creamy spinach gravy", 250, "palak_paneer.png"),

    # -------- Biryani --------
    ("Veg Biryani", "Aromatic basmati rice layered with mixed vegetables", 200, "veg_biryani.png"),
    ("Chicken Biryani", "Spicy dum cooked chicken and rice", 280, "chicken_biryani.png"),
    ("Mutton Biryani", "Rich long-grain rice with tender mutton pieces", 350, "mutton_biryani.png"),
    ("Hyderabadi Biryani", "Authentic style spicy biryani", 300, "hyderabadi_biryani.png"),
    ("Egg Biryani", "Layered rice with boiled eggs and spices", 220, "egg_biryani.png"),
]

def seed_menu():
    for name, desc, price, image in MENU_ITEMS:
        MenuItem.objects.get_or_create(
            name=name,
            defaults={
                "description": desc,
                "price": price,
                "image": f"menu/{image}"
            }
        )

    print("Menu seeded successfully.")
