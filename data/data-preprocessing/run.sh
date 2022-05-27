echo "install requirements.txt"
pip install -r requirements.txt
echo "data-preprocessing.ipynb to data-preprocessing.py"
jupyter nbconvert --to script data-preprocessing.ipynb
echo "interaction.ipynb to interaction.py"
jupyter nbconvert --to script interaction.ipynb
echo "run data-preprocessing.py"
python data-preprocessing.py
echo "run interaction.py"
python interaction.py
echo "run.sh terminated"