clean:
	find . -name '__pycache__' -delete
	find . -name "*.pyc" -delete

convert:
	jupyter nbconvert --to=html gsmls.ipynb
	jupyter nbconvert --to=html njmls.ipynb
