import csv
import re
import time
from datetime import datetime

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager


def nike_scrapper(url, gender, csv_file_name):

   
    # Utilisez ChromeDriveManager pour ouvrir le pilote Web afin d'éviter les problèmes de version
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    # Allez à la page que nous voulons scrape
    driver.get(url)

    # Cliquez sur le bouton États-Unis pour entrer le pays souhaité dans la fenêtre contextuelle    state_button = driver.find_element("xpath", '//button[@class="nav-btn p0-sm d-sm-b hf-geomismatch-btn-secondary hf-geomismatch-btn mt2-sm"]')
    state_button.click()
    time.sleep(2)
  
    # Revenir à la page que nous voulons scrape
    # driver.get("https://www.nike.com/w/mens-shoes-nik1zy7ok?sort=newest")
    driver.get(url)

    # Csv qui va stocker les données
    file_name = csv_file_name
    csv_file = open(file_name, 'w', encoding='utf-8', newline='')
    writer = csv.writer(csv_file)

    # Initialiser un dictionnaire vide pour les données
    product_dict = {}

    # Écrire les clés en haut du fichier
    product_dict['id_'] = ""
    product_dict['gender'] = ""
    product_dict['title'] = ""
    product_dict['url'] = ""
    product_dict['category'] = ""
    product_dict['price'] = ""
    product_dict['description'] = ""
    product_dict['description_long'] = ""
    product_dict['n_reviews'] = ""
    product_dict['score'] = ""
    product_dict['size'] = ""
    product_dict['comfort'] = ""
    product_dict['durability'] = ""
    product_dict['r_title'] = ""
    product_dict['r_raiting'] = ""
    product_dict['r_body'] = ""
    product_dict['r_date'] = ""
    writer.writerow(product_dict.keys())

    # Script pour faire défiler jusqu'à la fin du défilement infini pour charger tous les produits sur la page
    SCROLL_PAUSE_TIME = 2.0

    while True:

        
        # Obtenir la hauteur de défilement
        ### C'est la différence. Déplacer ceci * à l'intérieur * de la boucle
        ### signifie qu'il vérifie si scrollTo défile toujours 
        last_height = driver.execute_script("return document.body.scrollHeight")

        # Scroll jusqu'au bouton
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        # attandre le load de la page
        time.sleep(SCROLL_PAUSE_TIME)

        # Clicker sur 'X' pour fermer la pop-up
        try:
          close_button1 = driver.find_element("xpath", '//button[@class="pre-modal-btn-close bg-transparent"]')
          close_button1.click()
        except:
          pass

        # Calculer la nouvelle hauteur de défilement et comparer avec la dernière hauteur de défilement
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:

            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

            time.sleep(SCROLL_PAUSE_TIME)

            new_height = driver.execute_script("return document.body.scrollHeight")
          
            # vérifie si la hauteur de la page est restée la même
            if new_height == last_height:
                break
            # passez à la boucle suivante
            else:
                last_height = new_height
                continue

    # Clicker sur 'X' pour fermer la pop-up
    try:
        cookie_button = driver.find_element("xpath", '//*[@data-var="acceptBtn2"]')
        cookie_button.click()

        close_button1 = driver.find_element("xpath", '//button[@class="pre-modal-btn-close bg-transparent"]')
        close_button1.click()
    except:
        pass

    
    # Obtenir une liste de tous les produits sur la page en fonction de leur XPATH
    products = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.XPATH,
                                '//a[@class="product-card__link-overlay"]')))

    # Extraire l'URL de chacun des éléments produits
    urls = []
    for product in products:
        url = product.get_attribute('href')
        urls.append(url)

    # Obtenez le nombre total de produits et print pour comparer avec le nombre d'URL total_products = driver.find_element("xpath", '//span[@class="wall-header__item_count"]').get_attribute('textContent')
    total_products = re.findall('\d+', total_products)
    print("There are ", total_products, "products")
    print('We are scraping ', len(urls), "product urls")
    
    # Boucle sur tous les produits de la page
    index = 1

    for url in urls:
        # Clicker sur 'X' pour fermer la pop-up
        try:
            close_button1 = driver.find_element("xpath", '//button[@class="pre-modal-btn-close bg-transparent"]')
            close_button1.click()
        except:
            pass

        print("Scraping Product " + str(index))
        print(url)
        try:
            driver.get(url)
        except:
            continue
        id_ = index
        index = index + 1
        try:
            title = driver.find_element("xpath", '//h1[@id="pdp_product_title"]').get_attribute('textContent')
            category = driver.find_element("xpath", '//h2[@class="headline-5-small pb1-sm d-sm-ib css-1ppcdci"]').get_attribute('textContent')
            price = driver.find_element("xpath", '//div[@class="product-price is--current-price css-1emn094"]').get_attribute('textContent')
            price = int(re.findall('\d+', price)[0])
            description = driver.find_element("xpath", '//div[@class="description-preview body-2 css-1pbvugb"]/p').get_attribute('textContent')
            try:
                description_long = driver.find_element("xpath", '//div[@class="pi-pdpmainbody"]').get_attribute('textContent')
            except:
                try:
                    description_long = driver.find_element("xpath", '//div[@class="nby-product-desc-container"]').get_attribute('textContent')
                except:
                    description_long = ""
        except:
            print("Did not get info for product")
            title = ""
            category = ""
            price = ""
            description = ""
            description_long = ""

            # Essayez de cliquer sur le bouton de d'avis et sur le bouton plus s'il ne parvient pas à trouver xpath mettre l'avis comme vide        try:
        try:
            review_button = driver.find_element("xpath", "(//button[@class='css-1y5ubft panel-controls'])[2]")
            review_button.click()
            time.sleep(1)
            try:
                more_button = driver.find_element("xpath", '//label[@for="More Reviews"]')
                more_button.click()
                try:
                
                    # Obtenir un score moyen pour le produit
                    score = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH,
                                "//span[@class='TTavgRate']"))).get_attribute('textContent')
                    score = re.findall("\d+\.\d+", score)[0]

                    # Obtenir les informations du curseur
                    try:
                        sliders = WebDriverWait(driver, 2).until(EC.presence_of_all_elements_located((By.XPATH,
                                    '//div[@class="TT4reviewRangeDot"]')))[:3]
                        slider_data = [slider.get_attribute('style') for slider in sliders]
                        slider_data = [float(re.search('margin-left: calc\((.+)% - 5px\);', slider).group(1)) for slider in slider_data]
                    except:
                        size = ""
                        comfort = ""
                        durability = ""
                    try:
                        size = slider_data[0]
                        comfort = slider_data[1]
                        durability = slider_data[2]
                    except:
                        size = ""
                        comfort = ""
                        durability = ""

                    # Obtenir le nombre d'avis pour savoir combien de fois cliquer pour charger plus d'avis n_reviews = driver.find_element("xpath", '//div[@class="TTreviewCount"]').get_attribute('textContent')
                    n_reviews = driver.find_element("xpath", '//div[@class="TTreviewCount"]').get_attribute('textContent')
                    n_reviews = float((re.findall(("\d+.\d+|\d+"), n_reviews)[0]).replace(",", ""))
                    reviews_per_click = 20
                    times = (n_reviews // reviews_per_click)*1
                    print("There are ", n_reviews, "reviews")
                    print("Clicking load more", times, "times")
                    index1 = 0
                    # Boucle pour cliquer sur charger plus, en utilisant la fonction .execute_script car le bouton est masqué
                    while index1 < times:
                        try:
                            index1 += 1
                            load_more = WebDriverWait(driver, 1).until(EC.presence_of_element_located((By.XPATH,
                                                                                '//span[text()="Load More"]/..')))
                            driver.execute_script("arguments[0].click();", load_more)
                            time.sleep(0.3)
                            # Click on 'X' button to close news pop-up
                            try:
                                close_button1 = driver.find_element("xpath", '//button[@class="pre-modal-btn-close bg-transparent"]')
                                close_button1.click()
                            except:
                                continue
                        except:
                            continue

                    # Obtenir une liste de tous les avis à parcourir           
                    reviews = WebDriverWait(driver, 3).until(EC.presence_of_all_elements_located((By.XPATH,
                                '//div[@class="TTreview"]')))

                    for count, review in enumerate(reviews):

                        r_title = review.find_element("xpath", './/div[@class="TTreviewTitle"]').get_attribute('textContent')
                        r_raiting = float(review.find_element("xpath", './/meta[@itemprop="ratingValue"]').get_attribute('content'))
                        r_body = review.find_element("xpath", './/div[@class="TTreviewBody"]').get_attribute('textContent')
                        r_date = review.find_element("xpath", './/div[@itemprop="dateCreated"]').get_attribute('datetime')
                        r_date = datetime.strptime(r_date, '%Y-%m-%d')

                        product_dict['id_'] = id_
                        product_dict['gender'] = gender
                        product_dict['title'] = title
                        product_dict['url'] = url
                        product_dict['category'] = category
                        product_dict['price'] = price
                        product_dict['description'] = description
                        product_dict['description_long'] = description_long
                        product_dict['n_reviews'] = n_reviews
                        product_dict['score'] = score
                        product_dict['size'] = size
                        product_dict['comfort'] = comfort
                        product_dict['durability'] = durability
                        product_dict['r_title'] = r_title
                        product_dict['r_raiting'] = r_raiting
                        product_dict['r_body'] = r_body
                        product_dict['r_date'] = r_date
                        writer.writerow(product_dict.values())

                    print("Scrapped ", count+1, "reviews")

                except Exception as e:
                    print(type(e), e)
                    print(url)
            except:
                # S'il n'y a pas d'avis, enregistrez toutes les informations sur le produit mais laissez les champs d'avis vides                product_dict['id_'] = id_
                product_dict['gender'] = gender
                product_dict['title'] = title
                product_dict['url'] = url
                product_dict['category'] = category
                product_dict['price'] = price
                product_dict['description'] = description
                product_dict['description_long'] = description_long
                product_dict['n_reviews'] = ""
                product_dict['score'] = ""
                product_dict['size'] = ""
                product_dict['comfort'] = ""
                product_dict['durability'] = ""
                product_dict['r_title'] = ""
                product_dict['r_raiting'] = ""
                product_dict['r_body'] = ""
                product_dict['r_date'] = ""
                writer.writerow(product_dict.values())
        except:
            # S'il n'y a pas d'avis, enregistrez toutes les informations sur le produit mais laissez les champs d'avis vides            product_dict['id_'] = id_
            product_dict['gender'] = gender
            product_dict['title'] = title
            product_dict['url'] = url
            product_dict['category'] = category
            product_dict['price'] = price
            product_dict['description'] = description
            product_dict['description_long'] = description_long
            product_dict['n_reviews'] = ""
            product_dict['score'] = ""
            product_dict['size'] = ""
            product_dict['comfort'] = ""
            product_dict['durability'] = ""
            product_dict['r_title'] = ""
            product_dict['r_raiting'] = ""
            product_dict['r_body'] = ""
            product_dict['r_date'] = ""
            writer.writerow(product_dict.values())

    csv_file.close()
    driver.close()

# nike_scrapper("https://www.nike.com/w/mens-shoes-nik1zy7ok?sort=newest", "men", "nike_shoes_men.csv")

nike_scrapper("https://www.nike.com/w/womens-shoes-5e1x6zy7ok?sort=newest", "woman", "nike_shoes_woman.csv")