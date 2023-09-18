# Translate+

----------------------------------------------------------------------------------------------------------------------
## What is Translate+
This is a simple translate desktop app.
----------------------------------------------------------------------------------------------------------------------
### How to use Translate+
 1. Clone project:

    ` git clone https://github.com/Rinkoff/TranslatePlus.git`
 2. Install the necessary dependencies:
    ```
    cd TranslatePlus
    
    #Create your virtual environment for the project
    python -m venv .venv
    
    #Activate your virtual envinronment(Example:For Windows)
    .\.venv\Scripts\activate.bat
    
    #Install requirments
    pip install -r requirements.txt
    ```

 3. Create your own database and import it into the file directory:

   ` mysql -u root -p translateplus`

 4. Run Translate+.

    `python TranslatePlus.py`