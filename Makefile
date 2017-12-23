clean:
	find . -name '__pycache__' -delete
	find . -name "*.pyc" -delete

convert:
	jupyter nbconvert --to=html analysis.ipynb
