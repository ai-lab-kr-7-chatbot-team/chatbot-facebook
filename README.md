
# 실행방법

## 텔레그램 토큰 파일 생성.
vi flask_api_demo/.telelgram_token

## 도커뛰우기.
```bash
sh run-docker-compose.sh
docker rename chatbot-facebook_api_run_8602ee12544f chatbot-flask
```
## 도커 진입
docker exec -it chatbot-flask /bin/bash

## Flask 관련 모듈 설치 
sh install-python-dependencies.sh

## Flask 뛰우기 ( docker 내부 )
sh run-flask-api.sh

## 테스트
http://localhost:5000/tests/hello


## docker hub 로긴 ( https://hub.docker.com/ )
```bash
docker login
docker tag  python:latest mech12/chatbot-flask:1
docker push mech12/chatbot-flask:1
```

## postman api test
https://www.getpostman.com/collections/e13621d78a7a7c47bdec


## telegram webhook 
https://test-bot-fb.babyfriends.us/




# API Server with Docker + Flask-RESTful

## 1. Setting for Docker, Implementing Hello Api

- Initialized git
  ```
  .gitignore
  ```
- Dockerized python
  ```
  docker-compose.yml
  run-docker-compose.sh
  ```
- Installed python dependencies
  ```
  requirements.txt
  install-python-dependencies.sh
  ```
- Implemented simple api
  ```
  flask_api_demo/__init__.py
  run-flask-api.sh
  ```
- - -

## 2. Flask-RESTful + Blueprints

- Installed Flask_restful
- Implemented api with Flask-RESTful + Blueprints
- - -

## 3. Testing codes for authentication, authorization

- Set MongoDB container
- Configured for testing
- Wrote testing codes
- - -

## 4. Models + flask-jwt-extended

- Implemented models
- Introduction to JWT
- - -


## 5. Validation

- Introduction to marshmallow
- Implemented schemas
- - -






# telegram chatbot data sample
```js
payload = {'update_id': 280974475, 'message': {'message_id': 31, 'from': {'id': 43446854, 'is_bot': False, 'first_name': 'Roy', 'last_name': 'Cho', 'username': 'roy_cho', 'language_code': 'ko'}, 'chat': {'id': 43446854, 'first_name': 'Roy', 'last_name': 'Cho', 'username': 'roy_cho', 'type': 'private'}, 'date': 1606571726, 'text': 'hi'}}

payload = {'update_id': 280974479, 'edited_message': {'message_id': 40, 'from': {'id': 43446854, 'is_bot': False, 'first_name': 'Roy', 'last_name': 'Cho', 'username': 'roy_cho', 'language_code': 'ko'}, 'chat': {'id': 43446854, 'first_name': 'Roy', 'last_name': 'Cho', 'username': 'roy_cho', 'type': 'private'}, 'date': 1606572265, 'edit_date': 1606572312, 'text': 'hello'}}
```


# docker push 
```bash
docker login
docker tag python:latest  mech12/kogpt3-chatbot-flask:1
docker push mech12/kogpt3-chatbot-flask:1
```

# docker로 HIM chatbot 뛰우기.
```bash
docker pull mech12/kogpt2-chatbot-flask:1
docker run --rm -it -p 5001:5001 -p 5000:5000 mech12/kogpt2-chatbot-flask:1  /bin/bash
docker run -p 5001:5001 -p 5000:5000 mech12/kogpt2-chatbot-flask:1
docker rename [DOCKER NAMES]  kogpt2-chatbot-flask
docker exec -it kogpt2-chatbot-flask /bin/bash
```

