# FindlyAPI

**Этот API предоставляет функциональность для поиска товаров на различных маркетплейсах с возможностью фильтрации и
настройки параметров запроса.**

## Основной эндпоинт: `/api/search`

### Метод: `GET`

### Описание:

Этот эндпоинт выполняет поиск продуктов на нескольких маркетплейсах с учетом различных фильтров и параметров. Возвращает
JSON-ответ с результатами поиска, включая метаданные запроса.

---

### Параметры запроса

<table>
<tr><td>Параметр</td><td>Тип данных</td><td>Описание</td><td>Возможные значения</td><td>Обязателен ли</td></tr>
<tr><td><code>q</code></td><td><code>string</code></td><td>Запрос для поиска продуктов. Это основной параметр, который определяет, что искать.</td><td>Любая строка: <code>iPhone 13</code> ; <code>samsung s23</code> ; <code>xiaomi pad 6</code></td><td>Да</td></tr>
<tr><td><code>ms</code></td><td><code>int</code></td><td>Максимальное количество продуктов для возврата. Указывает максимальное количество товаров, которое будет возвращено.</td><td>Целое число от <code>1</code> до <code>40</code></td><td>Нет</td></tr>
<tr><td><code>on</code></td><td><code>string</code></td><td>Фильтр для показа только новых продуктов. Если включено, возвращаются только новые товары.</td><td><code>on</code> или <code>off</code> (по умолчанию <code>on</code>, если не указано)</td><td>Нет</td></tr>
<tr><td><code>pf</code></td><td><code>string</code></td><td>Фильтр для включения фильтрации по цене. Если указано, будет применена фильтрация продуктов по цене.</td><td><code>on</code> или <code>off</code> (по умолчанию <code>on</code>, если не указано)</td><td>Нет</td></tr>
<tr><td><code>nf</code></td><td><code>string</code></td><td>Фильтр для включения фильтрации по имени. Если указано, будет применена фильтрация по имени продукта.</td><td><code>on</code> или <code>off</code> (по умолчанию <code>on</code>, если не указано)</td><td>Нет</td></tr>
<tr><td><code>ew</code></td><td><code>string</code></td><td>Слово (или слова), которые необходимо исключить из результатов поиска. При необходимости указать несколько слов следует разделять их вертикальной чертой. Также слова, передаваемые в аргументе не должны содержаться в самом запросе, то есть в аргументе <code>q</code>. Если указан этот параметр, API исключит все товары, содержащие это слово.</td><td><code>pro</code><br/><code>pro|max|plus</code><br/><code>5g|4g|lite</code></td><td>Нет</td></tr>
</table>

---

### Примеры запроса

##### Поиск продуктов по запросу "iPhone 13" с максимальным количеством 10 продуктов.

```http
GET /api/search?q=iPhone+13&ms=10
```

##### Поиск только новых товаров "iPhone 13" с фильтрацией по цене.

```http
GET /api/search?q=iPhone+13&on=on&pf=on
```

##### Поиск продуктов "iPhone 13", исключая слово "refurbished".

```http
GET /api/search?q=iPhone+13&ew=refurbished
```

---

## Примеры тела ответа

### Успешный ответ (код 200)

Ответ включает два объекта: `products_data` (данные о продуктах) и `request_metadata` (метаданные запроса).

Пример ответа:

```json
{
  "products_data": {
    "MMG": [
      ...
    ],
    "Onliner": [
      ...
    ],
    "Kufar": [
      ...
    ],
    "21vek": [
      ...
    ]
  },
  "request_metadata": {
    "date": "12-17-2024 12:34:56",
    "response_time": 0.123,
    "size_of_products": {
      "all": 150,
      "mmg": 50,
      "onliner": 40,
      "kufar": 30,
      "21vek": 30
    },
    "request_args": {
      "max_size": 10,
      "only_new": true,
      "query": "iPhone 13",
      "enable_filter_by_price": true,
      "enable_filter_by_name": true,
      "exclusion_word": "refurbished"
    },
    "request_url": "http://localhost:5000/api/search?q=iPhone+13&ms=10",
    "response_code": 200
  }
}
```

Пример тела товара:

```json
{
  "image": "https://rms.kufar.by/v1/",
  "link": "https://www.kufar.by/item/",
  "name": "xiaomi 13 lite 256gb",
  "price": 390.0
}
```

### Неуспешный ответ (код, к примеру, 422)

```json
{
  "default_error": "422 Unprocessable Entity: The request was well-formed but was unable to be followed due to semantic errors.",
  "pretty_error": "Incorrect request parameters, read the API documentation https://github.com/koloideal/FindlyAPI/blob/main/README.md",
  "request_metadata": {
    "date": "12-17-2024 22:09:58",
    "request_url": "http://127.0.0.1:5000/api/search?pf=on&on=off&ew=air",
    "response_code": 422
  }
}
```

## Возможные ошибки ответа

| **Ошибка** | **Описание**                                  |
|------------|-----------------------------------------------|
| **405**    | **Метод не поддерживается для этого ресурса** |
| **404**    | **Не найден ресурс**                          |
| **403**    | **Доступ запрещен**                           |
| **422**    | **Некорректные параметры запроса**            |



