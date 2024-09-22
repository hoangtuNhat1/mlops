LOCAL_TAG:=$(shell date +"%Y-%m-%d-%H-%M")
LOCAL_IMAGE_NAME="stream-model-flower:${LOCAL_TAG}"
PREDICTIONS_STREAM_NAME='flower_predictions'
test: 
	pytest tests/ 
quality_checks: 
	isort . 
	black . 
build: quality_checks test 
	docker build -t ${LOCAL_IMAGE_NAME} .
intergration_test: build 
	LOCAL_IMAGE_NAME=${LOCAL_IMAGE_NAME} bash intergration-test/run.sh

publish: build 
	LOCAL_IMAGE_NAME=${LOCAL_IMAGE_NAME} bash scripts/publish.sh

setup: 
	pipenv install --dev 
	pre-commit install 