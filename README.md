# The "Asset Matcher" Interview Task
Domotz is looking for a talented, committed, and enthusiastic software engineer to take a pivotal role in expanding our product to greater heights.

To help us evaluate new talent, we have created this take-home interview question that should take you no more than a few hours.

**You must complete and submit the solution before the technical interview.**

### Why this interview format?
Traditional coding interviews can be intimidating and may not accurately reflect a candidate's abilities. By completing a take-home assignment, you can work in a more relaxed setting and demonstrate your true potential.

We aim is to ensure you feel comfortable and perform at your best.

### The Tech stack
At Domotz we are always striving to expand our tech stack but as specified in the job description the main languages/frameworks currently used include:
* Python
* JavaScript (TypeScript, NodeJS, AngularJS, React)

### The Task
We have provided you with two JSON files that contain information about Assets, both of which should contain an Asset's "Name", "Model", and "IP Address" but different naming conventions and formats:
* `Name` (Represented by 'name', 'name_snmp', 'asset-name')
* `Model` (Represented by 'model', 'asset-model')
* `IP Address` (Represented by 'ip_address', 'ipv4', 'ip-address')

In this repository you can find two sample data files:
* [`assets_1.json`](/assets_1.json).
* [`assets_2.json`](/assets_2.json).

##### Challenge Requirements
1. Create a web appication.
    1. Create a webpage that displays a table with the assets "Name, IP Address, Model" based on the contents in [`assets_1.json`](/assets_1.json). and [`assets_2.json`](/assets_2.json).
    2. The user should be presented an input field of free text and a submit button that will perform a matching with the assets' data fields in the above two json files based on the "Name", "Model" or "IP Address"
        The result of the submit button should display all three fields of the matched asset or "No Asset Found" in case it has failed to match anything
    
2. The system should be able to support:
    1. Larger sets of data (eg 10k+ assets)
    2. Different data formats - assets_1 and assets_2
    3. Asset 'Name', 'IP Address' and 'Model' Based matching
    4. If more than a single match is present it should match the first

3. Update the section `Installation and running this solution` in the README file explaining how to run your code

This task is aimed to evaluate your backend skills so do not worry about the UX and web application styles

### Submitting a solution
1. Clone this repository
2. Complete the problem outlined in the `Requirements` section
3. Create a new public repository under your github account with the solution (or private with with shared access with us)
4. Send us a link to your repository over email once ready

If you have any questions regarding requirements, do not hesitate to email your contact at Domotz for clarification.

### Installation and Running the Solution

This section provides step-by-step instructions to set up and run both the backend and frontend components of the application.

#### Project Structure

Below is the structure of the project directory:

```
/project-root-directory
│
├── app.py                    # Flask application entry point
├── requirements.txt          # Python dependencies
├── README.md                 # Documentation
├── /assets                   # Directory containing the JSON files
│   ├── assets_1.json         # Example JSON file 1
│   └── assets_2.json         # Example JSON file 2
│
├── /services                 # Directory containing service layer logic
│   └── asset_management.py   # Contains AssetProcessor, AssetManager, and AssetService classes
│
├── /tests                    # Directory containing backend tests
│   ├── test_app.py           # Tests for the Flask app (e.g., testing API routes)
│   └── test_asset_management.py # Tests for the asset management services
│
├── /asset-matcher            # Frontend directory (React application)
│   ├── package.json          # Node.js dependencies and scripts
│   ├── /src                  # Source directory for React components
│   │   ├── index.js          # React entry point
│   │   ├── App.js            # Main React component
│   └── /public               # Public directory for static assets
│       └── index.html        # HTML file for React app
```

#### 1. Clone the Repository

First, clone the repository to your local machine:

```bash
git clone <your-repo-url>
cd project-root-directory
```

#### 2. Setting Up the Backend (Flask)

1. **(Optional) Create a Virtual Environment:**

   It is recommended, but not required, to create a virtual environment to manage your dependencies:

   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

2. **Install Dependencies:**

   Install the Python packages listed in `requirements.txt`:

   ```bash
   pip install -r requirements.txt
   ```

3. **Run the Flask Application:**

   Start the Flask application by running:

   ```bash
   python app.py
   ```

   By default, the Flask server will run on `http://localhost:5000`.

   **Note:** If you have additional JSON files with assets, you can place them in the `/assets` directory. The application will automatically process and include them.

#### 3. Setting Up the Frontend (React)

1. **Navigate to the Frontend Directory:**

   Move to the frontend directory where the React application resides:

   ```bash
   cd frontend
   ```

2. **Install Node.js Dependencies:**

   Install the required packages using npm:

   ```bash
   npm install
   ```

3. **Run the React Application:**

   Start the React application:

   ```bash
   npm start
   ```

   The React application will run on `http://localhost:3000`.

#### 4. Accessing the Application

Once both the backend and frontend are running:

- Open a web browser and navigate to `http://localhost:3000`.
- The main page will display a table of assets fetched from the JSON files located in the `/assets` directory.
- Use the search bar to look up assets by their name, model, or IP address.

#### 5. Running Backend Tests

To ensure that the backend is functioning correctly, you can run the tests included in the `/tests` directory.

1. **Navigate to the project root directory:**

   ```bash
   cd project-root-directory
   ```

2. **Run the Tests:**

   Execute the tests using `pytest`:

   ```bash
   pytest
   ```

   This will run the tests defined in `test_app.py` and `test_asset_management.py`.

#### 6. Logging

Logs for the backend operations are written to both the console and the `app.log` file in the project root directory. These logs provide detailed information about the application’s operations, including asset processing and error handling.

#### Conclusion

By following the steps outlined above, you should be able to successfully set up, run, and interact with the Asset Matcher Web Application. If you encounter any issues or need further assistance, feel free to contact me.
