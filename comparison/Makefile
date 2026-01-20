.PHONY: build
build:
	docker build -t local-ml-runner .

.PHONY: run-local
run-local:
	docker run \                                                         ─╯
		-v "$(pwd):/data" \
		-e MY_CSV_FILE="/data/test_data_1000000.csv" \
		local-ml-runner python /data/job.py
