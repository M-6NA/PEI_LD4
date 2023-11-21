# PEI_LD4
# How to launch the application localy
!Python needs to be installed! <br>
1. Click on the green <>Code button and select download ZIP unzip the folder <br>
2. You will need to create a python virtual environment <br>
   In the same directory where the `1_Home.py` file open a terminal <br>
3. Write this command to create the virtual environment: <br>
   `python -m venv PEI_LD4_LIBS_3` <br>
4. Activate the environment: <br>
   `PEI_LD4_LIBS_3/Scripts/Activate` <br>
   !If need be to deactivate the env write this command to deactivate it!: <br>
   `deactivate` <br>
5. To install the necessary libraries (the env needs to be activated): <br>
   `pip install -r requirements.txt` <br>
   !This could take a while! <br>
6. To run the application run this command: <br>
   `streamlit run 1_Home.py` <br>
7. The application should open in the browser. Also there might be a prompt to allow streamlit to launch <br>

## About the file structure
- The `1_Home.py` is the landing page of the application
- All of the other files are in the pages folder
  
