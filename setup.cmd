# Install poppler utils as specified in <Project Root>/dependencies/pdf-apps/poppler

# Install python3 if not installed
python3 -m venv venv3
source venv3/bin/activate
pip3 install --upgrade pip
pip3 install -r requirements.txt

# For Monterey M1 Pro
ARCHFLAGS="-arch arm64e" CC=clang CXX=clang++ pip install pdftotext
