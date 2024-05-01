Allison Chan (6905922727)
Brandyn K. Lee (2422176714)
Eric Crouse (9271913867)

To run this project:
1. Clone this repository.
2. Create virtual environment to install dependencies for project and activate it.
3. From the cloned repository directory, install the requirements found in requirements.txt using “pip install -r requirements.txt”
4. Create new project on Firebase console. Under the “Build” drop-down menu, select “Realtime Database.”
5. On the Firebase console, go to the “Rules” tab under the Realtime Database created in step 4. Edit all “false” values to “true and click “Publish.” 
6. Go tthe “Data” tab and click on the icon with three vertical dots and select “IMPORT JSON.”  Select the “mushroom-default-rtdb-export.json” from the cloned repository.
7. Create 8 additional databases (only available with Blaze plan) and repeat step 5 for each.
8. Open “distribute_data.py” in a text editor and change the URLs in the dictionary labeled “DATABASE_URLS” with those created in step 7 and save.
9. Repeat step 8 for file “final_project.py”
10. Repeat step 8 for file “database_backend_mushroom.py” and also update “firebase_url” with the link to the default Firebase databse created in step 5 with “.json” added to the end of the reference url.
11. From the cloned repository direcotry as the root and virtual environment activated, from the command line, run “distribute_data.py”; this will populate the databases created in step 7 via a hashing function and requests library utilizing the Firebase REST API. Check Firebase console to confirm population.
12. From the Firebase console, for each database created in step 7, change the “Rules” to as follows and hit publish:
{
  "rules": {
    ".read": true,
    ".write": true,
    ".indexOn": ["bruises", "cap-color", "cap-shape", "cap-surface", "gill-attachment", "gill-color", "gill-size", "gill-spacing", "habitat", "odor", "poisonous", "population", "ring-number", "ring-type", "spore-print-color", "stalk-color-above-ring", "stalk-color-below-ring", "stalk-root", "stalk-shape", "stalk-surface-above-ring", "stalk-surface-below-ring", "veil-color", "veil-type"]
  }
}
13. Push to repository to deploy on streamlit. Make sure your have an account on Steamlit, and it is connected to our github. 


Files Included:
1. final_project.py
  This is where the streamlit website is being displayed. 
2. database_backend_mushroom.py
  This file is used by the database manager to run CRUD operations.
3. distribute_data.py
  This file is used for the initial upload of our data to our databases. 
4. mushroom-default-rtdb-export.json
  This file is used in step 6 of how to run this project providing key mapping information for attributes names and values.
5. requirements.txt
  This file is used to install necessary depenedencies to run project in virtual environment.

Front End:
Stremlit: In order to view content of final_project.py, please visit https://mushroom-identification.streamlit.app/.

Data Base Manager:
1. From the cloned repository directory as the root with the virtual environment actiivated, from the command line, run “python3 database_backend_mushroom.py”
2. Please follow instructions show in command line terminal to run CRUD operations.

