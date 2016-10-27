help:
	@echo "$(MAKE) [target]"
	@echo
	@echo "  targets:"
	@echo "    lint        - check style with flake8"
	@echo

lint:
	flake8
