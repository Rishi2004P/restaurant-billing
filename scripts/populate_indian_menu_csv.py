import pandas as pd
import os

def populate_indian_menu_to_csv():
    # Determine the base directory of the project
    base_dir = os.path.dirname(os.path.abspath(__file__))
    # Define the path for the menu.csv file
    csv_path = os.path.join(base_dir, '..', 'data', 'menu.csv')

    # Ensure the 'data' directory exists
    data_dir = os.path.dirname(csv_path)
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)
        print(f"Created directory: {data_dir}")

    # Expanded Sample Indian Menu Items (item_id, Name, Category, Price, GST%, Image URL)
    # Using placehold.co for placeholder images with item name
    indian_menu_items_data = [
        # Main Course (Curries & Gravies - Non-Veg)
        {"item_id": 1, "item_name": "Butter Chicken", "category": "Main Course (Non-Veg)", "price": 380.0, "gst": 5.0, "image_url": "https://sugarspunrun.com/wp-content/uploads/2025/04/Butter-chicken-1-of-1.jpg"},
        {"item_id": 2, "item_name": "Chicken Tikka Masala", "category": "Main Course (Non-Veg)", "price": 390.0, "gst": 5.0, "image_url": "https://i0.wp.com/www.nourishdeliciously.com/wp-content/uploads/2022/11/DSC_9207.jpg"},
        {"item_id": 3, "item_name": "Mutton Rogan Josh", "category": "Main Course (Non-Veg)", "price": 450.0, "gst": 5.0, "image_url": "https://static.toiimg.com/thumb/53192600.cms?width=1200&height=900"},
        {"item_id": 4, "item_name": "Fish Curry (Goan Style)", "category": "Main Course (Non-Veg)", "price": 420.0, "gst": 5.0, "image_url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQ67cX4YTCOGfflIGONRI9ZqaR6WN2ViWY8pQ&s"},
        {"item_id": 5, "item_name": "Prawn Malai Curry", "category": "Main Course (Non-Veg)", "price": 480.0, "gst": 5.0, "image_url": "https://static.toiimg.com/thumb/54439535.cms?imgsize=161358&width=800&height=800"},
        {"item_id": 6, "item_name": "Chicken Korma", "category": "Main Course (Non-Veg)", "price": 370.0, "gst": 5.0, "image_url": "https://www.errenskitchen.com/wp-content/uploads/2024/04/Chicken-Korma-1-16.jpg"},
        {"item_id": 7, "item_name": "Egg Curry", "category": "Main Course (Non-Veg)", "price": 250.0, "gst": 5.0, "image_url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQkchsX_ZF0YqunzrBg8ccqL2ki_UefvLMpBw&s"},
        # Main Course (Curries & Gravies - Veg)
        {"item_id": 8, "item_name": "Paneer Butter Masala", "category": "Main Course (Veg)", "price": 340.0, "gst": 5.0, "image_url": "https://cdn.zeptonow.com/production///tr:w-600,ar-100-100,pr-true,f-auto,q-80/web/recipes/paneer-butter-masala.png"},
        {"item_id": 9, "item_name": "Dal Makhani", "category": "Main Course (Veg)", "price": 290.0, "gst": 5.0, "image_url": "https://sinfullyspicy.com/wp-content/uploads/2015/03/4-1.jpg"},
        {"item_id": 10, "item_name": "Palak Paneer", "category": "Main Course (Veg)", "price": 310.0, "gst": 5.0, "image_url": "https://seitansociety.com/wp-content/uploads/2021/10/PalakPaneer1280x903.jpg"},
        {"item_id": 11, "item_name": "Malai Kofta", "category": "Main Course (Veg)", "price": 330.0, "gst": 5.0, "image_url":"https://i0.wp.com/myspicetrunk.com/wp-content/uploads/2021/01/20201219_1907582.jpg?resize=720%2C983&ssl=1"},
        {"item_id": 12, "item_name": "Navratan Korma", "category": "Main Course (Veg)", "price": 350.0, "gst": 5.0, "image_url": "https://www.deliciousmagazine.co.uk/wp-content/uploads/2023/10/2023D159_DIWALI_KORMA__-768x960.jpg"},
        {"item_id": 13, "item_name": "Aloo Gobi", "category": "Main Course (Veg)", "price": 260.0, "gst": 5.0, "image_url": "https://static01.nyt.com/images/2023/12/21/multimedia/ND-Aloo-Gobi-gkwc/ND-Aloo-Gobi-gkwc-mediumSquareAt3X.jpg"},
        {"item_id": 14, "item_name": "Bhindi Masala", "category": "Main Course (Veg)", "price": 270.0, "gst": 5.0, "image_url": "https://myfoodstory.com/wp-content/uploads/2025/03/Bhindi-Masala-2.jpg"},
        {"item_id": 15, "item_name": "Mushroom Do Pyaza", "category": "Main Course (Veg)", "price": 300.0, "gst": 5.0, "image_url": "https://coox-new.s3.ap-south-1.amazonaws.com/images/d/dishes/Mushroom%20do%20Pyaza-1-dish-img.jpeg?v=1734019293934"},
        {"item_id": 16, "item_name": "Chana Masala", "category": "Main Course (Veg)", "price": 240.0, "gst": 5.0, "image_url": "https://images.immediate.co.uk/production/volatile/sites/30/2020/08/chana-masala-fb809bc.jpg?quality=90&resize=440,400"},
        {"item_id": 17, "item_name": "Kadhai Paneer", "category": "Main Course (Veg)", "price": 320.0, "gst": 5.0, "image_url": "https://www.cubesnjuliennes.com/wp-content/uploads/2020/03/Best-Kadai-Paneer-Recipe.jpg"},
        {"item_id": 18, "item_name": "Mix Vegetable", "category": "Main Course (Veg)", "price": 280.0, "gst": 5.0, "image_url": "https://placehold.co/100x100/E0E0E0/333333?text=Mix+Vegetable"},
        {"item_id": 19, "item_name": "Dal Tadka", "category": "Main Course (Veg)", "price": 220.0, "gst": 5.0, "image_url": "https://www.indianhealthyrecipes.com/wp-content/uploads/2021/04/dal-tadka-recipe-500x500.jpg"},
        {"item_id": 20, "item_name": "Rajma Chawal (Combo)", "category": "Main Course (Veg)", "price": 200.0, "gst": 5.0, "image_url": "https://www.secondrecipe.com/wp-content/uploads/2017/08/rajma-chawal-1.jpg"},

        # Rice Dishes (Biryani & Pulao)
        {"item_id": 21, "item_name": "Hyderabadi Chicken Biryani", "category": "Rice Dish (Non-Veg)", "price": 400.0, "gst": 5.0, "image_url": "https://www.licious.in/blog/wp-content/uploads/2020/12/Hyderabadi-chicken-Biryani.jpg"},
        {"item_id": 22, "item_name": "Mutton Biryani", "category": "Rice Dish (Non-Veg)", "price": 480.0, "gst": 5.0, "image_url": "https://www.cubesnjuliennes.com/wp-content/uploads/2021/03/Best-Mutton-Biryani-Recipe.jpg"},
        {"item_id": 23, "item_name": "Egg Biryani", "category": "Rice Dish (Non-Veg)", "price": 320.0, "gst": 5.0, "image_url": "https://spicecravings.com/wp-content/uploads/2020/10/Egg-Biryani-Featured-1.jpg"},
        {"item_id": 24, "item_name": "Vegetable Biryani", "category": "Rice Dish (Veg)", "price": 300.0, "gst": 5.0, "image_url": "https://www.sharmispassions.com/wp-content/uploads/2022/03/VegBiryani4.jpg"},
        {"item_id": 25, "item_name": "Paneer Biryani", "category": "Rice Dish (Veg)", "price": 330.0, "gst": 5.0, "image_url": "https://happietrio.com/wp-content/uploads/2019/04/PaneerBiryani1.jpg"},
        {"item_id": 26, "item_name": "Kashmiri Pulao", "category": "Rice Dish (Veg)", "price": 280.0, "gst": 5.0, "image_url": "https://www.vegrecipesofindia.com/wp-content/uploads/2021/06/kashmiri-pulao-3.jpg"},
        {"item_id": 27, "item_name": "Peas Pulao", "category": "Rice Dish (Veg)", "price": 160.0, "gst": 5.0, "image_url": "https://www.indianveggiedelight.com/wp-content/uploads/2017/10/instant-pot-green-peas-pulao-featured.jpg"},
        {"item_id": 28, "item_name": "Jeera Rice", "category": "Rice Dish (Veg)", "price": 150.0, "gst": 5.0, "image_url": "https://mariasmenu.com/wp-content/uploads/Jeera-Rice-1.png"},
        {"item_id": 29, "item_name": "Plain Rice", "category": "Rice Dish (Veg)", "price": 100.0, "gst": 5.0, "image_url": "https://whatscooking.org.in/admin/uploads/product/6016Plain%20Rice%20(JPEG)%20(1).jpg"},
        {"item_id": 30, "item_name": "Lemon Rice", "category": "Rice Dish (Veg)", "price": 180.0, "gst": 5.0, "image_url": "https://www.flavourstreat.com/wp-content/uploads/2020/12/turmeric-lemon-rice-recipe-02.jpg"},

        # Breads
        {"item_id": 31, "item_name": "Naan (Plain)", "category": "Bread", "price": 50.0, "gst": 0.0, "image_url": "https://static.toiimg.com/thumb/53338316.cms?width=1200&height=900"},
        {"item_id": 32, "item_name": "Butter Naan", "category": "Bread", "price": 55.0, "gst": 0.0, "image_url": "https://foodess.com/wp-content/uploads/2023/02/Butter-Naan-2.jpg"},
        {"item_id": 33, "item_name": "Garlic Naan", "category": "Bread", "price": 60.0, "gst": 0.0, "image_url": "https://zestfulkitchen.com/wp-content/uploads/2020/01/garlic-naan-hero_for-web-4-683x1024.jpg"},
        {"item_id": 34, "item_name": "Cheese Naan", "category": "Bread", "price": 80.0, "gst": 0.0, "image_url": "https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEgqEhg-noHtRDYRrgh72EezX2Zv0mMwREkPY34GcFBkjnUUceMcLxgaiblNoElRvmk2EbNW_19C8P1zKR74lIKsZHAwMJeZvS50e_oaDZ8j-1NPbhYjcpxYQWq1uOSu0fOkVbu3rL__MVxt/s1600/Cheese+Naan3.jpg"},
        {"item_id": 35, "item_name": "Tandoori Roti", "category": "Bread", "price": 30.0, "gst": 0.0, "image_url": "https://maharajaroyaldining.com/wp-content/uploads/2024/05/Tandoori-Roti-3.webp"},
        {"item_id": 36, "item_name": "Butter Roti", "category": "Bread", "price": 35.0, "gst": 0.0, "image_url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSGHVVbp6cPUqd14HEQ5VkuFYK0he5gPtc48w&s"},
        {"item_id": 37, "item_name": "Laccha Paratha", "category": "Bread", "price": 70.0, "gst": 0.0, "image_url": "https://www.whiskaffair.com/wp-content/uploads/2020/06/Lachha-Paratha-2-3-500x500.jpg"},
        {"item_id": 38, "item_name": "Aloo Paratha", "category": "Bread", "price": 90.0, "gst": 5.0, "image_url": "https://cookingfromheart.com/wp-content/uploads/2020/09/Aloo-Paratha-4.jpg"},
        {"item_id": 39, "item_name": "Pudina Paratha", "category": "Bread", "price": 75.0, "gst": 0.0, "image_url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSFCisNxM6q8G1E7M3blP1ypollZURVhvQAsA&s"},
        {"item_id": 40, "item_name": "Missi Roti", "category": "Bread", "price": 45.0, "gst": 0.0, "image_url": "https://img-global.cpcdn.com/steps/0dcaeb49b7fc029a/400x400cq80/photo.jpg"},

        # South Indian
        {"item_id": 41, "item_name": "Masala Dosa", "category": "South Indian", "price": 130.0, "gst": 5.0, "image_url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQSj4XhJE3LJLqeFVQ65SqvLBp43p4BCRSz1w&s"},
        {"item_id": 42, "item_name": "Plain Dosa", "category": "South Indian", "price": 100.0, "gst": 5.0, "image_url": "https://static.toiimg.com/thumb/53239433.cms?imgsize=247810&width=800&height=800"},
        {"item_id": 43, "item_name": "Rava Dosa", "category": "South Indian", "price": 140.0, "gst": 5.0, "image_url": "https://moonrice.net/wp-content/uploads/2021/05/IMG_0938-2.jpg"},
        {"item_id": 44, "item_name": "Paneer Dosa", "category": "South Indian", "price": 160.0, "gst": 5.0, "image_url": "https://www.cookclickndevour.com/wp-content/uploads/2019/01/paneer-masala-dosa-recipe-1.jpg"},
        {"item_id": 45, "item_name": "Mysore Masala Dosa", "category": "South Indian", "price": 150.0, "gst": 5.0, "image_url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQ9tXNH_xCEYOU9wjkNFLKfCHUf1mvc8QmR4g&s"},
        {"item_id": 46, "item_name": "Idli Sambar (2 pcs)", "category": "South Indian", "price": 100.0, "gst": 5.0, "image_url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQm7TA6mFE2Qs_KuFNQ_jrfTXqTGfQxWnoZyg&s"},
        {"item_id": 47, "item_name": "Medu Vada (2 pcs)", "category": "South Indian", "price": 90.0, "gst": 5.0, "image_url": "https://vps029.manageserver.in/test/wp-content/uploads/2023/12/u113o4r_medu-vada_625x300_06_September_23.jpg"},
        {"item_id": 48, "item_name": "Uttapam (Onion)", "category": "South Indian", "price": 120.0, "gst": 5.0, "image_url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRR25bExlo45LjjwUU9y9e4y82HGJyFbOGd8A&s"},
        {"item_id": 49, "item_name": "Tomato Uttapam", "category": "South Indian", "price": 125.0, "gst": 5.0, "image_url": "https://www.tarladalal.com/media/onion-tomato-uttapam-recipe.webp"},
        {"item_id": 50, "item_name": "Curd Rice", "category": "South Indian", "price": 140.0, "gst": 5.0, "image_url": "https://palatesdesire.com/wp-content/uploads/2022/04/curd-rice-recipe-card@palates-desire.jpg"},
        {"item_id": 51, "item_name": "Pongal", "category": "South Indian", "price": 110.0, "gst": 5.0, "image_url": "https://www.indianveggiedelight.com/wp-content/uploads/2021/11/ven-pongal-featured.jpg"},

        # Street Food / Snacks
        {"item_id": 52, "item_name": "Vada Pav", "category": "Street Food", "price": 65.0, "gst": 5.0, "image_url": "https://www.cookwithmanali.com/wp-content/uploads/2018/04/Vada-Pav-500x500.jpg"},
        {"item_id": 53, "item_name": "Pani Puri (6 pcs)", "category": "Street Food", "price": 80.0, "gst": 5.0, "image_url": "https://img.clevup.in/368842/SKU-0058_0-1735613906627.jpg?width=600&format=webp"},
        {"item_id": 54, "item_name": "Samosa (2 pcs)", "category": "Street Food", "price": 75.0, "gst": 5.0, "image_url": "https://cdn.zeptonow.com/production/tr:w-640,ar-2400-2400,pr-true,f-auto,q-80/cms/product_variant/9b412081-6d87-42ed-b484-12ec32afe634.jpeg"},
        {"item_id": 55, "item_name": "Pav Bhaji", "category": "Street Food", "price": 160.0, "gst": 5.0, "image_url": "https://www.cubesnjuliennes.com/wp-content/uploads/2020/07/Instant-Pot-Mumbai-Pav-Bhaji-Recipe.jpg"},
        {"item_id": 56, "item_name": "Dabeli", "category": "Street Food", "price": 70.0, "gst": 5.0, "image_url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcT8ebpMEvZqBi4tovpv4-gWqW9M0j7VgjZIgg&s"},
        {"item_id": 57, "item_name": "Bhel Puri", "category": "Street Food", "price": 90.0, "gst": 5.0, "image_url": "https://vegecravings.com/wp-content/uploads/2018/06/Bhel-Puri-Recipe-Step-By-Step-Instructions-500x500.jpg"},
        {"item_id": 58, "item_name": "Sev Puri", "category": "Street Food", "price": 95.0, "gst": 5.0, "image_url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQx6_4CtgEtJSoTBj3Ly2Zf6YwulhOOo4fb1w&s"},
        {"item_id": 59, "item_name": "Aloo Tikki", "category": "Street Food", "price": 85.0, "gst": 5.0, "image_url": "https://sinfullyspicy.com/wp-content/uploads/2023/03/1-1.jpg"},
        {"item_id": 60, "item_name": "Kachori", "category": "Street Food", "price": 70.0, "gst": 5.0, "image_url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQqO0ieyO6huc4rGemgOq5lK5L-66kFU7BwPA&s"},
        {"item_id": 61, "item_name": "Pakora Platter", "category": "Street Food", "price": 150.0, "gst": 5.0, "image_url": "https://d2e1hu1ktur9ur.cloudfront.net/wp-content/uploads/2022/07/Tea-Time-Pakora-Platter-_Fe.jpg"},

        # Tandoor & Grills (Starters / Appetizers)
        {"item_id": 62, "item_name": "Chicken Tikka (6 pcs)", "category": "Tandoor & Grills", "price": 320.0, "gst": 5.0, "image_url": "https://www.awesomecuisine.com/wp-content/uploads/2014/03/chicken-tikka.jpg"},
        {"item_id": 63, "item_name": "Paneer Tikka (6 pcs)", "category": "Tandoor & Grills", "price": 290.0, "gst": 5.0, "image_url": "https://rotibotionline.com/wp-content/uploads/2024/03/paneer-tikka-scaled.jpg"},
        {"item_id": 64, "item_name": "Tandoori Chicken (Half)", "category": "Tandoor & Grills", "price": 350.0, "gst": 5.0, "image_url": "https://kitchenlaughter.com/wp-content/uploads/2022/09/grilled-half-chicken-12.jpg"},
        {"item_id": 65, "item_name": "Seekh Kebab (Chicken, 4 pcs)", "category": "Tandoor & Grills", "price": 300.0, "gst": 5.0, "image_url": "https://derafarms.com/cdn/shop/files/deraproducts-2024-06-12T110804.251.png?v=1719207183"},
        {"item_id": 66, "item_name": "Malai Boti (Chicken, 6 pcs)", "category": "Tandoor & Grills", "price": 330.0, "gst": 5.0, "image_url": "https://www.chilitochoc.com/wp-content/uploads/2022/11/one-malai-boti-skewer.jpg"},
        {"item_id": 67, "item_name": "Mushroom Tikka (6 pcs)", "category": "Tandoor & Grills", "price": 280.0, "gst": 5.0, "image_url": "https://www.vegrecipesofindia.com/wp-content/uploads/2013/08/mushroom-tikka-recipe-11.jpg"},

        # Soups
        {"item_id": 68, "item_name": "Tomato Soup", "category": "Soup", "price": 120.0, "gst": 5.0, "image_url": "https://www.onceuponachef.com/images/2021/02/Tomato-Soup-3-1200x1800.jpg"},
        {"item_id": 69, "item_name": "Sweet Corn Soup (Veg)", "category": "Soup", "price": 130.0, "gst": 5.0, "image_url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSC2FeSWsl8T37Q9QVI0Q8m4AnB7ox6RwnQwg&s"},
        {"item_id": 70, "item_name": "Hot & Sour Soup (Chicken)", "category": "Soup", "price": 150.0, "gst": 5.0, "image_url": "https://www.cookingcarnival.com/wp-content/uploads/2023/09/Hot-and-sour-soup-4.jpg"},

        # Salads & Raita
        {"item_id": 71, "item_name": "Green Salad", "category": "Accompaniment", "price": 80.0, "gst": 5.0, "image_url": "https://leelalicious.com/wp-content/uploads/2018/08/Corn-Tomato-Avocado-Salad-Recipe.jpg"},
        {"item_id": 72, "item_name": "Cucumber Raita", "category": "Accompaniment", "price": 90.0, "gst": 5.0, "image_url": "https://spicedspoon.com/wp-content/uploads/2024/09/cucumber-raita.webp"},
        {"item_id": 73, "item_name": "Boondi Raita", "category": "Accompaniment", "price": 95.0, "gst": 5.0, "image_url": "https://www.whiskaffair.com/wp-content/uploads/2020/12/Boondi-Raita-2-3.jpg"},
        {"item_id": 74, "item_name": "Papad (Roasted)", "category": "Accompaniment", "price": 30.0, "gst": 5.0, "image_url": "https://gurukripahotel.com/wp-content/uploads/2025/04/Roasted-Papad.png"},

        # Desserts
        {"item_id": 75, "item_name": "Gulab Jamun (2 pcs)", "category": "Dessert", "price": 110.0, "gst": 5.0, "image_url": "https://lalaji.com.au/wp-content/uploads/2025/01/Gulab-Jamun.webp"},
        {"item_id": 76, "item_name": "Gajar Halwa", "category": "Dessert", "price": 130.0, "gst": 5.0, "image_url": "https://www.whiskaffair.com/wp-content/uploads/2019/05/Gajar-Ka-Halwa-2-3.jpg"},
        {"item_id": 77, "item_name": "Kulfi (Pista)", "category": "Dessert", "price": 90.0, "gst": 5.0, "image_url": "https://static.toiimg.com/thumb/84786580.cms?width=1200&height=900"},
        {"item_id": 78, "item_name": "Rasgulla (2 pcs)", "category": "Dessert", "price": 100.0, "gst": 5.0, "image_url": "https://www.mygovindas.com/uploads/food_menu/rasgula-485b24065d63ab10b4745be1af423f6e.jpg"},
        {"item_id": 79, "item_name": "Jalebi (with Rabri)", "category": "Dessert", "price": 140.0, "gst": 5.0, "image_url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcS78ovpXDHxtGEoNEqxizuENorFcIY0KH-x5Q&s"},

        # Beverages
        {"item_id": 80, "item_name": "Mango Lassi", "category": "Beverage", "price": 100.0, "gst": 5.0, "image_url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRlSlQ45vH_JReiUTNXyYvVMwW6Lb5G05fLRA&s"},
        {"item_id": 81, "item_name": "Sweet Lassi", "category": "Beverage", "price": 90.0, "gst": 5.0, "image_url": "https://www.sharmispassions.com/wp-content/uploads/2023/08/sweet-lassi3.jpg"},
        {"item_id": 82, "item_name": "Salted Lassi", "category": "Beverage", "price": 90.0, "gst": 5.0, "image_url": "https://themagicsaucepan.com/wp-content/uploads/2018/05/20180511-salt-lassi-0061-500x500.jpg"},
        {"item_id": 83, "item_name": "Masala Chai", "category": "Beverage", "price": 60.0, "gst": 5.0, "image_url": "https://masalaandchai.com/wp-content/uploads/2021/07/Masala-Chai.jpg"},
        {"item_id": 84, "item_name": "Filter Coffee", "category": "Beverage", "price": 70.0, "gst": 5.0, "image_url": "https://img.onmanorama.com/content/dam/mm/en/food/features/images/2024/3/9/filter-coffee-1.jpg?w=1120&h=583"},
        {"item_id": 85, "item_name": "Fresh Lime Soda (Sweet)", "category": "Beverage", "price": 80.0, "gst": 5.0, "image_url": "https://www.seriouseats.com/thmb/Lkr5DnY7jNP2aP5DS3d5qE0PEkQ=/1500x0/filters:no_upscale():max_bytes(150000):strip_icc()/__opt__aboutcom__coeus__resources__content_migration__serious_eats__seriouseats.com__2020__08__20200816-nimbu-soda-vicky-wasik-1-28079d5d45ee4e47a37a969d1e4834a0.jpg"},
        {"item_id": 86, "item_name": "Fresh Lime Soda (Salted)", "category": "Beverage", "price": 80.0, "gst": 5.0, "image_url": "https://brainfoodstudio.com/wp-content/uploads/2015/08/sweety-salty-fresh-lime-soda-4.jpg"},
        {"item_id": 87, "item_name": "Jaljeera", "category": "Beverage", "price": 70.0, "gst": 5.0, "image_url": "https://www.whiskaffair.com/wp-content/uploads/2019/03/Jaljeera-2-1.jpg"},
        {"item_id": 88, "item_name": "Bottled Water (1L)", "category": "Beverage", "price": 20.0, "gst": 0.0, "image_url": "https://images-cdn.ubuy.co.in/64d6094fb48aa21d8f6389e3-aquafina-purified-bottled-drinking.jpg"},
        {"item_id": 89, "item_name": "Soft Drink (Cola)", "category": "Beverage", "price": 50.0, "gst": 5.0, "image_url": "https://media.istockphoto.com/id/1393991948/photo/cola-with-crushed-ice-in-glass-and-there-is-water-droplets-around-cool-black-fresh-drink.jpg?s=612x612&w=0&k=20&c=St-ONdM6Tpg_DPFzZzq-OI-dsIG2Hv30KVdYf83ARs8="},
        {"item_id": 90, "item_name": "Buttermilk (Chaas)", "category": "Beverage", "price": 70.0, "gst": 5.0, "image_url": "https://www.awesomecuisine.com/wp-content/uploads/2008/11/masala-buttermilk.jpg"},

        # Combos / Thalis
        {"item_id": 91, "item_name": "Veg Thali (Standard)", "category": "Combo", "price": 280.0, "gst": 5.0, "image_url": "https://bsmedia.business-standard.com/_media/bs/img/article/2023-10/10/full/20231010102653.jpg"},
        {"item_id": 92, "item_name": "Veg Thali (Deluxe)", "category": "Combo", "price": 350.0, "gst": 5.0, "image_url": "https://www.theskburger.com/wp-content/uploads/2023/02/e1dad5315972c8a9db86fb01d69c7ecb.jpg"},
        {"item_id": 93, "item_name": "Non-Veg Thali (Chicken)", "category": "Combo", "price": 380.0, "gst": 5.0, "image_url": "https://i0.wp.com/vps029.manageserver.in/menu/wp-content/uploads/2024/01/indian-gavkari-chicken-thali-food-600nw-2017167788.webp?fit=600%2C450&ssl=1"},
        {"item_id": 94, "item_name": "Non-Veg Thali (Mutton)", "category": "Combo", "price": 450.0, "gst": 5.0, "image_url": "https://i.ytimg.com/vi/W_cnf3eMDnc/hq720.jpg?sqp=-oaymwEhCK4FEIIDSFryq4qpAxMIARUAAAAAGAElAADIQj0AgKJD&rs=AOn4CLAqBA6x2NhK6--UDYSIFdeqThUJQQ"},
        {"item_id": 95, "item_name": "Dosa Combo (Dosa, Idli, Vada)", "category": "Combo", "price": 200.0, "gst": 5.0, "image_url": "https://t4.ftcdn.net/jpg/02/17/39/75/360_F_217397519_MqLzfynUsUKGvZj1AB3iPREmr11sYRhk.jpg"},
        {"item_id": 96, "item_name": "Biryani Combo (Biryani, Raita, Salad)", "category": "Combo", "price": 420.0, "gst": 5.0, "image_url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQGKeu_tWel5wWuD3qXzc8dk_Z1P6qM2b18QA&s"},

        # Snacks / Breakfast (Additional)
        {"item_id": 97, "item_name": "Poha", "category": "Breakfast/Snacks", "price": 80.0, "gst": 5.0, "image_url": "https://media.istockphoto.com/id/670526200/photo/poha-indian-snacks.jpg?s=612x612&w=0&k=20&c=iEVKSfRzmcHxPIz1fKQBNzmcRpLbseh5vjXaRVckRZA="},
        {"item_id": 98, "item_name": "Upma", "category": "Breakfast/Snacks", "price": 85.0, "gst": 5.0, "image_url": "https://myfoodstory.com/wp-content/uploads/2022/11/Vegetable-Upma-4.jpg"},
        {"item_id": 99, "item_name": "Misal Pav", "category": "Breakfast/Snacks", "price": 120.0, "gst": 5.0, "image_url": "https://www.foodie-trail.com/wp-content/uploads/2021/12/PHOTO-2021-11-01-08-19-11_1-rotated.jpg"},
        {"item_id": 100, "item_name": "Kanda Bhaji", "category": "Breakfast/Snacks", "price": 70.0, "gst": 5.0, "image_url": "https://images.getrecipekit.com/20221104111936-dussehrafestivefoodskandabhajiimage5.jpg?aspect_ratio=1:1&quality=90"},
    ]

    try:
        # Create a pandas DataFrame from the list of dictionaries
        df = pd.DataFrame(indian_menu_items_data)

        # Save the DataFrame to a CSV file
        df.to_csv(csv_path, index=False)
        print(f"Successfully saved {len(indian_menu_items_data)} Indian menu items to {csv_path}")

    except Exception as e:
        print(f"An error occurred while writing to CSV: {e}")

if __name__ == "__main__":
    populate_indian_menu_to_csv()