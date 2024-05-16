conda env list
conda activate py39

pip install -r requirements.txt

streamlit run .\Dashboard.py

sebelum deploy di sreamlit, pastikan depedency berikut di hapus dari requirement.txt
tensorflow-estimator==2.13.0
tensorflow-intel==2.13.0
tensorflow-io-gcs-filesystem==0.31.0