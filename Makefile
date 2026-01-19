# Load .env file
ifneq (,$(wildcard .env))
  include .env
  export
endif

.PHONY: run
run:
	echo $$IMAGE
	echo $$TAG

.PHONY: docker-push
docker-push:
	docker buildx build \
		--platform linux/amd64,linux/arm64 \
		--push \
		-f Dockerfile \
		-t ${IMAGE}:${TAG} \
		. \
		--sbom=true \
		--provenance=true
	@echo ${IMAGE}
	@echo ${TAG}