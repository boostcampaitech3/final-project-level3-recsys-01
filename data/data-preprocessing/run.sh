echo "install requirements.txt"
pip install -r requirements.txt
echo "data-preprocessing.ipynb to data-preprocessing.py"
jupyter nbconvert --to script data-preprocessing.ipynb
echo "splitted_dataset.ipynb to splitted_dataset.py"
jupyter nbconvert --to script splitted_dataset.ipynb
echo "run data-preprocessing.py"
python data-preprocessing.py
echo "run splitted_dataset.py"
python splitted_dataset.py
echo "run.sh terminated"