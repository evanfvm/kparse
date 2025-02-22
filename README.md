
# KPARSE

Parsing tools for Ericsson RAN ENM kget logs
Webapp written with Streamlit
Window app with TKinker, wrapped by pyinstaller


## Author: Bao Pham

- [@evanfvm](https://www.github.com/evanfvm)


## License

[MIT](https://choosealicense.com/licenses/mit/)


## Dependencies

- python (>=3.13.1,<3.14)
- pyinstaller (>=6.12.0,<7.0.0)


  *Requirement Python Packages*
- streamlit (>=1.42.0,<2.0.0)
- pandas (>=2.2.3,<3.0.0)
- numpy (>=2.2.3,<3.0.0)
- openpyxl (>=3.1.5,<4.0.0)
- watchdog (>=6.0.0,<7.0.0)


## Usage/Examples

1. Install dependency with poetry (if having poetry)
`poetry install`
`poetry shell`

2. Start web app
`streamlit run kparse.py`

3. Start Tkinker app
`python eran.py`

4. Package Tkinker app
`pyinstaller --onefile --windowed --icon 'images\eran-icon.png' eran.py`
--> Make sure to copy folder 'images\' into 'dist\eran\' to ensure app run correctly.
