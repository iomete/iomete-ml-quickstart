docker_image := iomete/sample-job
docker_tag := 1.0.0

install-requirements:
	pip install -r infra/requirements.txt

run-job:
	python job.py
	
docker-build:
	# Run this for one time: docker buildx create --use
	docker build -f infra/Dockerfile -t ${docker_image}:${docker_tag} .
	@echo ${docker_image}
	@echo ${docker_tag}

docker-push:
	# Run this for one time: docker buildx create --use
	docker buildx build --platform linux/amd64,linux/arm64 --push -f infra/Dockerfile -t ${docker_image}:${docker_tag} .
	@echo ${docker_image}
	@echo ${docker_tag}