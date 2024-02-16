test:
	pytest

coverage:
	scripts/run_coverage.sh

docker:
	scripts/build_docker_images.sh

release-patch:
	scripts/release_topicaxisapi.sh patch

release-minor:
	scripts/release_topicaxisapi.sh minor
