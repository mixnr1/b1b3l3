import requests
from bs4 import BeautifulSoup
url = 'https://bibele.lv/bibele/bibele.php'
response = requests.get(url)
if response.status_code == 200:
    soup = BeautifulSoup(response.content, 'html.parser')
    select_element = soup.find('select', {'class': 'booktitle'})
    books_dict = {}
    if select_element:
        for option in select_element.find_all('option'):
            value = option['value']
            text = option.get_text(strip=True)
            books_dict[value] = text
        for key in books_dict:
            url = 'https://www.bibele.lv/bibele/bibele.php'
            post_data = {
                'query': '',
                'book_select': key,  
                'chapter_select': '1',  
                'current_mode': 'reference',
                'book': key,  
                'chapter': '1',  
                'verse': '0',
                'topic': '',
                'search_mode': 'C',
                'last_view': 'reference',
                'page': '1',
                'type': 'bible',
                'view': 'area'
            }
            response = requests.post(url, data=post_data)
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                select_element = soup.find('select', class_='chaptertitle')
                chapter_values = []
                if select_element:
                    for option in select_element.find_all('option'):
                        chapter_values.append(option['value'])
                for elem in chapter_values:
                    print(f"[{books_dict[key]} - {elem}. nodaļa]")
                    url = 'https://www.bibele.lv/bibele/bibele.php'
                    post_data = {
                        'query': '',
                        'book_select': key,  
                        'chapter_select': elem,  
                        'current_mode': 'reference',
                        'book': key,  
                        'chapter': elem,  
                        'verse': '0',
                        'topic': '',
                        'search_mode': 'C',
                        'last_view': 'reference',
                        'page': '1',
                        'type': 'bible',
                        'view': 'area'
                    }
                    response = requests.post(url, data=post_data)
                    soup = BeautifulSoup(response.content, 'html.parser')
                    table_element = soup.find('table', class_='normal')
                    if table_element:
                        first_span = table_element.find('span', class_='normal')
                        if first_span:
                            for br in first_span.find_all('br'):
                                br.replace_with('\n')
                            print(first_span.get_text())
                            # print(first_span.get_text(strip=True))
                        else:
                            print("No <span class='normal'> element found in the first <table class='normal'>.")
                    else:
                        print("No <table class='normal'> element found.")
                else:
                    print(f"[{books_dict[key]}]")
                    soup = BeautifulSoup(response.content, 'html.parser')
                    table_element = soup.find('table', class_='normal')
                    if table_element:
                        first_span = table_element.find('span', class_='normal')
                        if first_span:
                            for br in first_span.find_all('br'):
                                br.replace_with('\n')
                            print(first_span.get_text())
                            # print(first_span.get_text(strip=True))
                        else:
                            print("No <span class='normal'> element found in the first <table class='normal'>.")
                    else:
                        print("No <table class='normal'> element found.")
        else:
            print(f"POST request failed. Status code: {response.status_code}")
else:
    print(f"Failed to retrieve the webpage. Status code: {response.status_code}")