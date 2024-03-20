for tests
```
docker compose -f compose.test.yaml up -d --build && docker logs --follow test_web_fastapi && docker compose -f compose.test.yaml down -v
```

for web

```
docker compose -f compose.web.yaml up -d --build
```

```
docker compose -f compose.web.yaml down -v
```
