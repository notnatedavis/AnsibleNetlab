#   Makefile

.PHONY: deploy configure test destroy all

deploy:
	./scripts/deploy.sh

configure:
	./scripts/configure.sh

test:
	./scripts/test.sh

destroy:
	./scripts/destroy.sh

all: deploy configure test