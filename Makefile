proto:
	mkdir -p src/python/sky_atc/generated/
	python -m grpc_tools.protoc -Isrc/proto --python_out=src/python/sky_atc/generated --grpc_python_out=src/python/sky_atc/generated src/proto/pod_provider.proto
	sed -i "" "s/import pod_provider_pb2/import sky_atc\.generated\.pod_provider_pb2/g" src/python/sky_atc/generated/pod_provider_pb2_grpc.py

test: proto
	python -m pip install -e . pytest
	pytest -v src/python/tests

docker: proto
	docker build -t sky-atc:dev .

kind: docker
	kind load docker-image sky-atc:dev


test-runpod: proto
	python -m pip install -e .[runpod]
	pytest -v src/python/integration_tests/test_runpod.py

test-modal: proto
	python -m pip install -e .[modal]
	pytest -v src/python/integration_tests/test_modal.py
