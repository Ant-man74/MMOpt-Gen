CC=python3
EXEC= pytest main

all: $(EXEC)

pytest: ## Launch pytest and all unit test that it can find
	pytest

main: ## Execute the main genetic algorythm
	$(CC) main.py

clean: ## Clean the whole project
	rm -rf geneticAlgo/__pycache__
	rm -rf geneticAlgo/*.pyc
	rm -rf test/__pycache__
	rm -rf test/*.pyc

cleanTest: ## Clean the test package
	rm -rf test/__pycache__/  
	rm -rf test/*.pyc 

cleanGen: ## Clean the geneticAlgo package
	rm -rf /geneticAlgo/__pycache__
	rm -rf /geneticAlgo/*.pyc

install: ## Install dependency
	pip install lxml
	pip install numpy
	pip install matplotlib
	
installTravis: ## Install dependency for Travis io
	pip install lxml
	pip install matplotlib

help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

