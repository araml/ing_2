PYTHON = python3

help:
	@echo "Uso: make [options]"
	@echo "Opciones:"
	@echo "  tests        	corre todos los tests que pide el taller"
	@echo "  genetic      	corre 10 iteraciones del algoritmo genetico variando la semilla"
	@echo "  genetic-rep  	corre 10 iteraciones del algoritmo genetico con semillas fijas"

tests:
	@echo "Tests"

genetic:
	@echo "Genetico"

genetic-rep:
	@echo "Genetico rep"
