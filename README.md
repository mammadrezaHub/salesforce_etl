## Salesforce ETL
### Background

**Salesforce ETL** is a simple web app that helps you turn Salesforce files into clean, usable data without needing to write complex SQL and import to Amdaris Salesforce.

It guides you step by step through loading files, shaping the data, and preparing it for export in a clear and visual way.

### What the App Does

The app guides you through a simple, structured ETL flow:

1. **Load**  
   Upload one or more source files (`CSV`, `XLS`, `XLSX`) and assign aliases to each file.

2. **Transform**  
   Define transformations using:
   - Column **mapping** (including expressions)
   - Optional **joins**
   - Optional **filters** (`WHERE`)
   - Optional **grouping** (`GROUP BY`)

3. **Generate**  
   Automatically generates a clean, formatted SQL `SELECT` statement based on your configuration.

4. **Export & Reuse**  
   Save and load transformation configurations as JSON files to reuse or iterate on ETL logic.


## Running the App
The app is started using a single script named **`salesforce`**, which sets up the environment and runs the application automatically.
> On the first run, installing dependencies may take a few minutes. Subsequent runs will be much faster.

### Prerequisites
- Install **Python 3** from https://www.python.org/downloads/ and ensure it is added to PATH


### Windows
- Double-click `salesforce.cmd`


### macOS
- Open Terminal in the project folder.
- Allow the script to run (one time only):
```bash
chmod +x salesforce
```
- Double-click `salesforce.command`


### Linux
- Navigate to the project folder:
- Allow the script to run (one time only):
```bash
chmod +x salesforce
```
- Execute the app
```bash
./salesforce.command
```