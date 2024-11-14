python -m venv env_gpu
call env_gpu\Scripts\activate.bat
python -m pip install --upgrade pip
pip install -r requirements-gpu.txt
python -m gaming_coach
