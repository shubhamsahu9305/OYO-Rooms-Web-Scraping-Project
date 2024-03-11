import requests
from bs4 import BeautifulSoup
import pandas as pd

headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.3; Win 64 ; x64) Apple WeKit /537.36(KHTML , like Gecko) '
                        'Chrome/80.0.3987.162 Safari/537.36'}

hotel_name = []

hotel_address = []

hotel_rating = []

hotel_reviews_num = []

hotel_review = []

hotel_price = []

hotel_price_tax = []

for i in range(1, 27):
    print(i)
    try:
        url = "https://www.oyorooms.com/hotels-in-delhi/?page={}".format(i)
        webpage = requests.get(url,headers=headers)
        print("STATUS CODE",webpage.status_code)
    except Exception as e:
        print(e)

    html_code = BeautifulSoup(webpage.text, "lxml")

    boxes = html_code.find_all("div", {"class": "hotelCardListing__descriptionWrapper"})

    for box in boxes:
        # print(box)
        name = box.find("h3", {"class": "listingHotelDescription__hotelName d-textEllipsis"})
        hotel_name.append(name.text)
    print(len(hotel_name))

    for box in boxes:
        address = box.find("span", {"class": "u-line--clamp-2", "itemprop": "streetAddress"})
        hotel_address.append(address.text)
    print(len(hotel_address))

    for box in boxes:
        rating = box.find("div", {"class": "hotelRating__wrapper"})
        if rating is None:
            hotel_rating.append(0)
        else:
            hotel_rating.append(float(rating.span.text))
    print(len(hotel_rating))

    for box in boxes:
        reviews = box.find("span", {"class": "hotelRating__ratingSummary"})
        if reviews is None:
            hotel_reviews_num.append("No Reviews")
        else:
            hotel_reviews_num.append(reviews.text)
    print(len(hotel_reviews_num))

    for box in boxes:
        review = box.find_all("span", {"class": "hotelRating__ratingSummary"})
        if review is None or review == []:
            hotel_review.append("New")
        else:
            hotel_review.append(review[1].text)
    print(len(hotel_review))

    for box in boxes:
        price = box.find("span", {"class": "listingPrice__finalPrice"})
        if price is None:
            hotel_price.append("Sold Out")
        else:
            hotel_price.append(price.text)
    print(len(hotel_price))

    for box in boxes:
        price_tax = box.find("div", {"class": "listingPrice__perRoomNight"})
        if price_tax is None:
            hotel_price_tax.append("Sold Out")
        else:
            hotel_price_tax.append(price_tax.span.text)
    print(len(hotel_price_tax))

hotel_dict = {"Hotel Name": hotel_name, "Address": hotel_address, "Price": hotel_price, "Taxes": hotel_price_tax,
              "Rating": hotel_rating, "Number of Reviews": hotel_reviews_num, "Rating_Grade": hotel_review}
df_oyo_hotels = pd.DataFrame(hotel_dict)

df_oyo_hotels.to_excel("OYO_NewDelhi_hotel_detail.xlsx")

print(df_oyo_hotels)
