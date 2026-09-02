.PHONY: run serve doctor issue test build

run:
	python -m agentpassport serve

serve:
	python -m agentpassport serve

doctor:
	python -m agentpassport doctor

issue:
	python -m agentpassport issue --name $$(NAME) --owner $$(OWNER)

build:
	python -m pip install -e .

test:
	python -m pytest tests -q

web:
	cd web/react && npm install && npm run dev
