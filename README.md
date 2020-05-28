# Alternative_Exam_Fourier
Discrete math exam project about Fast Fourier Transform (FFT) and music key analysis

# How to use (windows):

- You can download Main.zip, but I recommend you to clone directory /Interface/dist/main to be up to date )
- Do you have *.wav file? (If not get it)
- Rename your *.wav file in Music.wav
- Throw your Music.wav in /Interface/dist/main (Name of file MUST be Music.wav)
- Run main.exe (In same directory as Music.wav)
- Enjoy! :)

# How to Develop:

**You need:**
- Python ~ v3.7
- PyQt5
- NumPy
- PyQtGraph
- pyinstaller (to bulid executable)

**How to run:**
- Open Interface directory
- In main.py in Signal constructor{signal=Signal("~~Your file.wav~~")} write file you want to analyze
- Run main.py

**How to buid executable**
- Run in PowerShall\Console when in root folder(Interface) : 
pyinstaller --add-data="GUI.ui;." --add-data="program.py;." main.py
- Throw Music.wav in dist/main, run main.exe in same dir
Name must be Music.wav!!