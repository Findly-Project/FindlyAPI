# FindlyAPI

**API для поиска товаров на различных маркетплейсах с возможностью гибкой фильтрации и настройки параметров запроса.**

---

## Основной эндпоинт: `/api/search`

### Метод: `POST`

Этот эндпоинт выполняет поиск продуктов на нескольких маркетплейсах. Параметры поиска и фильтрации передаются в теле запроса в формате JSON. В ответ возвращается JSON с результатами поиска и метаданными запроса.

---

### Тело запроса (Request Body)

Тело запроса должно быть в формате `application/json` и соответствовать следующей структуре:


| Параметр | Тип | Описание | Значение по умолчанию | Обязательный |
| :-- | :-- | :-- | :-- | :-- |
| `query` | `string` | Поисковый запрос. Основной параметр, определяющий, что искать. | — | **Да** |
| `max_size` | `integer` | Максимальное количество товаров для возврата с каждого маркетплейса. | `20` | Нет |
| `exclude_marketplaces` | `array[string]` | Список маркетплейсов, которые нужно исключить из результатов поиска. | `[]` | Нет |
| `filters` | `object` | Объект с дополнительными фильтрами для уточнения поиска. | `{}` | Нет |

#### Вложенные параметры в `filters`:

| Параметр | Тип | Описание | Значение по умолчанию |
| :-- | :-- | :-- | :-- |
| `only_new` | `boolean` | Если `true`, в результатах будут только новые товары. | `false` |
| `name_filter` | `boolean` | Включает дополнительную фильтрацию по названию товара. | `false` |
| `price_filter` | `boolean` | Включает дополнительную фильтрацию по цене товара. | `false` |
| `exclude_words` | `array[string]` | Список слов, которые нужно исключить из названий товаров в результатах поиска. | `[]` |


---

### Примеры запросов

**Пример тела запроса (JSON)**

Поиск "iPhone 12" с максимальным размером выборки 20, с исключением маркетплейсов "MMG" и "21vek":

```json
{
  "query": "iphone 12",
  "max_size": 20,
  "exclude_marketplaces": ["MMG", "21vek"],
  "filters": {
    "only_new": false,
    "name_filter": false,
    "price_filter": false,
    "exclude_words": ["pro"]
  }
}
```

**Пример запроса с помощью cURL**

```bash
curl -X 'POST' \
  'http://127.0.0.1:8000/api/search' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "query": "string",
  "max_size": 20,
  "exclude_marketplaces": ["MMG", "Onliner", "21vek", "Kufar"],
  "filters": {
    "only_new": false,
    "name_filter": false,
    "price_filter": false,
    "exclude_words": []
  }
}'
```


---

## Примеры ответов сервера

#### Успешный ответ (код 200)

Ответ содержит два основных ключа: `products_data` с найденными товарами, сгруппированными по маркетплейсам, и `request_metadata` с информацией о запросе.

**Пример ответа:**

```json
{
  "products_data": {
    "Onliner": [
      {
        "image": "https://imgproxy.onliner.by/...",
        "link": "https://catalog.onliner.by/mobile/apple/iphone12",
        "name": "Apple iPhone 12 64GB (черный)",
        "price": 1385.0
      }
    ],
    "Kufar": [
      {
        "image": "https://rms.kufar.by/v1/...",
        "link": "https://www.kufar.by/item/1021695505",
        "name": "чехол на айфон 12",
        "price": 3.0
      }
    ]
  },
  "request_metadata": {
    "date": "06-18-2025 18:15:45",
    "request_args": {
      "query": "iphone 12",
      "max_size": 20,
      "exclude_marketplaces": [
        "MMG",
        "21vek"
      ],
      "filters": {
        "only_new": false,
        "name_filter": false,
        "price_filter": false,
        "exclude_words": [
          "pro"
        ]
      }
    },
    "request_url": "/api/search",
    "response_code": 200,
    "response_time": 1.5221
  }
}
```


## Негативные ответы сервера

**Ошибка валидации (код 422 - Unprocessable Entity)**

Эта ошибка возникает, если тело запроса не соответствует схеме: например, отсутствует обязательное поле или тип данных неверный.

**Причина:** Отсутствует обязательное поле `query`.

```json
{
    "response_code": 422,
    "pretty_error": "Incorrect request parameters, read the API documentation https://github.com/koloideal/FindlyAPI/blob/main/README.md",
    "specific_error": [
        {
            "error_type": "missing",
            "error": {
                "error_field": "query",
                "error_msg": "Missing required field"
            }
        }
    ],
    "request_metadata": {
        "date": "06-18-2025 20:10:04",
        "request_url": "/api/search"
    }
}
```

**Причина:** Неверный тип данных для поля `max_size` (ожидается `integer`, передан `string`).

```json
{
    "response_code": 422,
    "pretty_error": "Incorrect request parameters, read the API documentation https://github.com/koloideal/FindlyAPI/blob/main/README.md",
    "specific_error": [
        {
            "error_type": "validation",
            "error": {
                "error_field": "max_size",
                "error_msg": "Input should be a valid integer"
            }
        }
    ],
    "request_metadata": {
        "date": "06-18-2025 20:10:41",
        "request_url": "/api/search"
    }
}
```

**Причина:** Метод запроса не разрешён (`POST` единственный разрешенный)

```json
{
    "response_code": 405,
    "default_error": "Method Not Allowed",
    "pretty_error": "Request method not allowed",
    "request_metadata": {
        "date": "06-18-2025 20:21:28",
        "request_url": "/api/search"
    }
}
```

<div style="display: flex">
    <div>MIT 2025</div><div style="position: absolute; right: 0">made by kolo</div>
</div>

