python -m venv env_cpu
call env_cpu\Scripts\activate.bat

python -m pip install --upgrade pip
pip install -r requirements-cpu.txt --extra-index-url=https://download.pytorch.org/whl/cpu

cls
echo Run 'python -m gaming_coach' (no quotes) to start!
