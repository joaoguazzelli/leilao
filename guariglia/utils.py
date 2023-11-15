import pandas as pd

def build_item(items, lots):
    for lot in lots:
        item = {}

        text = find_attribute('Marca/Modelo', lot)

        manufacturer, model = get_model_and_manufacturer(text)
        item['manufacturer'] = manufacturer
        item['model'] = model

        text = find_attribute('Ano/Modelo', lot)
        item['year'] = text

        text = find_attribute('Combustível', lot)
        item['gas'] = text

        text = find_attribute('KM', lot)
        item['km'] = text

        text = find_attribute('Despesas', lot)
        item['expenses'] = text

        text = find_last_bid(lot)
        item['last_bid'] = text

        items.append(item)
    return items


def find_attribute(keyword, lot):
    aux = lot.find('b', text=lambda text: text and keyword in text)
    if aux:
        text = aux.find_next_sibling(text=True)
        if text:
            return text


def find_last_bid(lot):
    text = lot.find('div', {'class': 'lance_atual'})
    if text:
        return text.text


def get_model_and_manufacturer(text):
    try:
        aux = text.split('/')
        manufacturer = aux[0]
        model = aux[1]
        return manufacturer, model
    except:
        return '', ''
def save_csv(items):
    df = pd.DataFrame(items)
    df.to_csv('guariglia_result.csv', index=False)
