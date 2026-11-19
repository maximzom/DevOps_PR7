# Автоматизована перевірка контейнеризованого сервісу локально та у CI

Проєкт демонструє багаторівневу автоматизовану перевірку контейнеризованого вебсервісу Nginx (`devops_7-homework`) за допомогою інфраструктурних тестів (`pytest-testinfra`), зовнішніх HTTP-перевірок (`pytest`), CLI-скрипту моніторингу (`check_service.py`) та конвеєра **GitHub Actions**.


## Підготовка середовища

```bat
python -m venv .venv
.venv\Scripts\activate
python -m pip install -r requirements.txt
```

## Збірка та запуск контейнера

```bat
docker build -t devops7-service .
docker run -d --name devops7-web -p 127.0.0.1:8080:80 devops7-service
```

Перевірка маршрутів вручну:

```bat
curl.exe -i --max-time 5 http://127.0.0.1:8080/
curl.exe -i --max-time 5 http://127.0.0.1:8080/health.json
curl.exe -i --max-time 5 http://127.0.0.1:8080/missing-page
```

## Запуск автоматичних перевірок

```bat
set BASE_URL=http://127.0.0.1:8080
set EXPECTED_RELEASE=devops_7-homework
set CHECK_TIMEOUT=3

python -m pytest tests/unit -v
python -m pytest --hosts=docker://devops7-web tests/infra -v
python -m pytest tests/http -v
python check_service.py
```

Коди завершення `check_service.py`:
- `0` — сервіс доступний і містить очікуваний `EXPECTED_RELEASE`;
- `1` — помилка HTTP-запиту або невідповідність версії релізу;
- `2` — перевищено час очікування (`CHECK_TIMEOUT`).

## Очищення середовища

```bat
docker rm -f devops7-web
```