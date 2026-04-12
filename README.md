# Catalog Service

## Быстрый старт

### Клонирование репозитория

```bash
git clone git@github.com:Esposus/catalog-test.git
cd catalog-test
```

## Состав проекта
- **Вопросы по SQL и дизайну БД** – папка `sql/`
- **REST API** – добавление товара в заказ

### Запуск в Docker rest api сервера

```bash
docker compose up --build
```

После сборки образов и запуска контейнеров сервис будет доступен на localhost на порту 8000:

Openapi документация: http://localhost:8000/docs

### Остановка сервиса

```bash
docker compose down -v
```

### Примечание

При первом запуске автоматически создаются тестовые клиент c id = 1 и категория c id = 1, если таблицы пусты.

Ссыкла на [тестовое задание](https://docs.google.com/document/d/1IXCY12SSbktV2XM_X9tuIdnfpj1ZEnN05wCOhef5wpk/edit?pli=1&tab=t.0)
