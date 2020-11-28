
# 실행방법

## 도커뛰우기.
sh run-docker-compose.sh
docker rename chatbot-facebook_api_run_8602ee12544f chatbot-flask

## 도커 진입
docker exec -it chatbot-flask /bin/bash

## Flask 관련 모듈 설치 
sh install-python-dependencies.sh

## Flask 뛰우기 ( docker 내부 )
sh run-flask-api.sh

## 테스트
http://localhost:5000/tests/hello


## docker hub 로긴 ( https://hub.docker.com/ )
docker login
docker tag  python:latest mech12/chatbot-flask:1
docker push mech12/chatbot-flask:1


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
