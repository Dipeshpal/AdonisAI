pyarmor obfuscate --restrict=0 decision_maker_api.py
python setup.py sdist bdist_wheel
twine upload dist/*twine upload dist/*