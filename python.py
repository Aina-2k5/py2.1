from selenium import webdriver
from selenium.webdriver.common.by import By
import json
from time import sleep

driver = webdriver.Chrome()
driver.get('http://books.toscrape.com/index.html')

knigi = []
thirst_url = None

for page in range(1, 6):
    print(f"Страница {page}")
    sleep(1)

    books = driver.find_elements(By.CSS_SELECTOR, "article.product_pod")
    for book in books:
        try:
            title_element = book.find_element(By.CSS_SELECTOR, "h3 a")
            title = title_element.get_attribute("title")
            price = book.find_element(By.CLASS_NAME, "price_color").text
            nalichie = book.find_element(By.CLASS_NAME, "instock").text.strip()

            if "thirst" in title.lower():
                thirst_url = title_element.get_attribute("href")

            knigi.append({
                "название": title,
                "цена": price,
                "наличие": nalichie
            })
        except Exception:
            continue

    try:
        next_btn = driver.find_element(By.LINK_TEXT, "next")
        next_btn.click()
        sleep(1)
    except:
        break

with open("books.json", "w", encoding="utf-8") as f:
    json.dump(knigi, f, ensure_ascii=False, indent=2)

print(f"Данные о {len(knigi)} книгах сохранены в books.json")

if thirst_url:
    print("Открываем книгу 'Thirst'...")
    driver.get(thirst_url)
    sleep(2)
    driver.save_screenshot("thirst.png")
    print("Скриншот книги 'Thirst' сохранён как 'thirst.png'")
else:
    print("Книга 'Thirst' не найдена — скриншот не сделан.")

driver.quit()
print("Готово.")