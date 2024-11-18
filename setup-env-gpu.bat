python -m venv env_gpu
call env_gpu\Scripts\activate.bat

python -m pip install --upgrade pip
pip install -r requirements-gpu.txt --extra-index-url=https://download.pytorch.org/whl/cu124

cls
echo Run 'python -m gaming_coach' (no quotes) to start!
