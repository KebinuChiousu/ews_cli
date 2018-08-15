clean:
	rm -rf ./dist
	rm -rf ews_cli.egg-info
dist:
	python3 setup.py sdist
release:
	twine upload dist/*	
