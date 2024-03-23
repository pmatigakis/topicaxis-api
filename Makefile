test:
	pytest

coverage:
	scripts/run_coverage.sh

docker:
	scripts/build_docker_images.sh

release-patch:
	scripts/release_api.sh patch

release-minor:
	scripts/release_api.sh minor
