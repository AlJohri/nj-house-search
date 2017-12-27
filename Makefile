.PHONY: clean

all:
	jupyter nbconvert --to=notebook --inplace --ExecutePreprocessor.enabled=True --ExecutePreprocessor.timeout=0 gsmls.ipynb
	jupyter nbconvert --to=notebook --inplace --ExecutePreprocessor.enabled=True --ExecutePreprocessor.timeout=0 njmls.ipynb
	jupyter nbconvert --to=notebook --inplace --ExecutePreprocessor.enabled=True --ExecutePreprocessor.timeout=0 cjmls.ipynb
	jupyter nbconvert --to=html gsmls.ipynb
	jupyter nbconvert --to=html njmls.ipynb
	jupyter nbconvert --to=html cjmls.ipynb

clean:
	find . -name '__pycache__' -delete
	find . -name "*.pyc" -delete
