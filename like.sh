curl -X 'POST' \
  'http://127.0.0.1:8000/api/v1/likes/' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "article_id": 100,
  "user_id": '$1'
}'