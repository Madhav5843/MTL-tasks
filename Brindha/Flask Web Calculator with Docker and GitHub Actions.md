# Flask Web Calculator with Docker and GitHub Actions

DevOps Learning Notes | Python • Flask • Git • GitHub • Docker • CI/CD

These notes are organized step by step so you can use them for learning, practical implementation, revision, and DevOps interview preparation.

## 1. Project Overview

Project name: Flask Calculator App

Objective: Build a simple web calculator using Python and Flask, package it into a Docker container, store the source code in GitHub, and automate code validation and Docker image building using GitHub Actions.

### Technologies used

[Python logo Icons, Logos, Symbols – Free Download PNG, SVG](https://images.openai.com/static-rsc-4/DmsB8FS-GP7uphH6D36okAKArZlBuv18j7laB7MGQztxtnElBP3iuvRtFFsgJN3_CMjTR795lNP5nkz0C0O5HRM_6vUhOfMDScUzQErc9yfIrgdVyj38VLAdNtbsn3vWhJAUhRcvYx9LUssqXM5zJvcGr4rSiP0dNojMqKdTlnc?purpose=inline)

Python + Flask

Write the backend logic and serve the calculator web page.

[Git アイコン、ロゴ、シンボル – 無料ダウンロード PNG、SVG](https://images.openai.com/static-rsc-4/Sb9O7jvMvZHvARi9aABeXIsBR0rd39FouCmFfFC--ZTHNXo79OH1i9deenC1xIJDeNhErgpYvCNupQ86CyufXxgmC_VQuaWQJaVMQ1Bu_NZ1pz9CTE0V2o-hLrSXkvABahTtp3cJmsi0qPnuLXNK6XMJdccgzbVA2YTQJZF6slM?purpose=inline)

Git + GitHub

Track code changes and host the source code repository.

[docker Logo PNG Vector (SVG) Free Download](https://images.openai.com/static-rsc-4/R3tE02yQDDdrIl6Y80p2egXN6vwiSR9hKiNlew9xJDHhHCd8CZixMDiOe_pHIFhQZOscJaB4FYXNP06W9P60nxIT5jsSVnyIMRI3Gj2fry6bJ-Z1UcJzVLjvbHqfUZXJNpiT7V7Yl9VplHUBGs4QsgfSbR35dVUxWHcDx7_FPyg?purpose=inline)

Docker

Package the application and its dependencies into an image and run it in a container.

[Android GitHub Actions Setup - DEV Community](https://images.openai.com/static-rsc-4/sePLPBbLKTTDogXXdhHYIZwXrS0oAzLVMDOla8Evt2VCbBeqb5TY_hC2VLa05QCUim_e1eZraJzxzXm_-MSaaPmnoc1u5RLtouaA96v3rvn_HE_XPMoS8KLyvdySVER7a1fpgCKSw0op0ShXc0Ve-udY8QxrSvIPPAh3-JXza2s?purpose=inline)

GitHub Actions

Automatically validate the Python code and build the Docker image when code is pushed.

### How the project works

1\. Develop the application

Python + Flask + HTML + CSS

2\. Push code to GitHub

Git repository • dev branch

3\. GitHub Actions runs

Install dependencies → validate Python → build Docker image

4\. Docker image is built

The image can be run locally or published to a registry.

Important: This project demonstrates Continuous Integration (CI) and Docker image building. It does not yet deploy the application to a server automatically, so it is not a complete Continuous Deployment (CD) pipeline.

## 2. Project Folder Structure

Create a folder named `calculator-app` and organize the files as follows:

```
calculator-app/
│
├── app.py
├── requirements.txt
├── Dockerfile
├── .dockerignore
├── README.md
│
├── templates/
│   └── index.html
│
├── static/
│   └── style.css
│
└── .github/
    └── workflows/
        └── build.yml
```

### Purpose of each file

| File or folder                | Purpose                                                  |
| ----------------------------- | -------------------------------------------------------- |
| `app.py`                      | Flask application and calculator logic                   |
| `requirements.txt`            | Python package dependencies                              |
| `Dockerfile`                  | Instructions to build the Docker image                   |
| `.dockerignore`               | Excludes unnecessary files from the Docker build context |
| `README.md`                   | Project documentation and setup instructions             |
| `templates/index.html`        | Calculator web page                                      |
| `static/style.css`            | Web page styling                                         |
| `.github/workflows/build.yml` | GitHub Actions CI workflow                               |

Remember: Flask automatically looks for HTML templates inside the `templates/` folder and static assets such as CSS inside the `static/` folder by default.

## 3. Create the Flask Application: `app.py`

Purpose: This file contains the backend logic that receives user input, performs calculations, handles errors, and sends the result back to the HTML page.

```
from flask import Flask, render_template, requestapp = Flask(__name__)@app.route("/", methods=["GET", "POST"])def calculator():    result = None    error = None    if request.method == "POST":        try:            num1 = float(request.form["num1"])            num2 = float(request.form["num2"])            operation = request.form["operation"]            if operation == "add":                result = num1 + num2            elif operation == "subtract":                result = num1 - num2            elif operation == "multiply":                result = num1 * num2            elif operation == "divide":                if num2 == 0:                    error = "Cannot divide by zero"                else:                    result = num1 / num2        except ValueError:            error = "Please enter valid numbers"    return render_template(        "index.html",        result=result,        error=error    )if __name__ == "__main__":    app.run(host="0.0.0.0", port=5000)
```

### Explanation

- `Flask(__name__)`: Creates the Flask application.
- `@app.route("/")`: Defines the home page URL.
- `methods=["GET", "POST"]`: Allows the page to load and receive form submissions.
- `request.form`: Retrieves values submitted by the HTML form.
- `float()`: Converts input into numbers that support decimal values.
- `if/elif`: Selects the requested mathematical operation.
- `render_template()`: Loads the HTML template and passes the result or error to it.
- `host="0.0.0.0"`: Allows the application to accept connections through its network interfaces, which is important for Docker port mapping.
- `port=5000`: Runs the Flask development server on port 5000.

## 4. Create the HTML Page: `templates/index.html`

Purpose: Creates the user interface where users enter numbers, choose an operation, and view the result.

```
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Flask Calculator</title>
    <link rel="stylesheet"
          href="{{ url_for('static', filename='style.css') }}">
</head>

<body>
    <div class="container">
        <h1>🧮 Flask Calculator</h1>

        <form method="POST">
            <input type="number" step="any" name="num1"
                   placeholder="Enter Number 1" required>

            <input type="number" step="any" name="num2"
                   placeholder="Enter Number 2" required>

            <select name="operation">
                <option value="add">Addition</option>
                <option value="subtract">Subtraction</option>
                <option value="multiply">Multiplication</option>
                <option value="divide">Division</option>
            </select>

            <button type="submit">Calculate</button>
        </form>

        {% if result is not none %}
            <h2 class="success">Result: {{ result }}</h2>
        {% endif %}

        {% if error %}
            <h2 class="error">{{ error }}</h2>
        {% endif %}
    </div>
</body>
</html>
```

### Important concepts

- HTML creates the structure of the web page.
- The `form` sends user input to the Flask backend.
- `method="POST"` submits the data to the server.
- `name="num1"`, `name="num2"` and `name="operation"` identify the submitted fields.
- `url_for('static', filename='style.css')` links the CSS file correctly.
- `{{ result }}` displays the calculation result.
- `{% if %}` is Jinja template syntax used to conditionally display results and errors.

## 5. Create the CSS File: `static/style.css`

Purpose: Makes the calculator visually appealing by adding colors, spacing, layout, and styling.

```
body {
    background: #f5f7fa;
    font-family: Arial, sans-serif;
}

.container {
    width: 90%;
    max-width: 450px;
    margin: 80px auto;
    background: white;
    padding: 30px;
    border-radius: 12px;
    box-shadow: 0 0 15px rgba(0, 0, 0, 0.1);
    box-sizing: border-box;
}

h1 {
    text-align: center;
    color: #333;
}

input,
select,
button {
    width: 100%;
    padding: 12px;
    margin-top: 10px;
    box-sizing: border-box;
}

button {
    background: #0078d4;
    color: white;
    border: none;
    cursor: pointer;
}

button:hover {
    background: #005ea6;
}

.success {
    color: green;
}

.error {
    color: red;
}
```

Key takeaway: HTML provides the structure, CSS controls the appearance, and Python with Flask handles the calculation logic.

## 6. Create `requirements.txt`

This file lists the Python packages required by the application.

```
Flask==3.0.3
```

### Install the dependencies

Open PowerShell or your terminal in the project directory.

```
python -m pip install -r requirements.txt
```

Check the installed Flask version:

```
python -m flask --version
```

Why is `requirements.txt` important?

It allows developers and automated pipelines to install the same specified package versions instead of installing dependencies manually one by one.

## 7. Create the Dockerfile

Purpose: Defines how Docker builds a container image for the Flask application.

Create a file named `Dockerfile` without a file extension.

```
FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["python", "app.py"]
```

### Explanation of each instruction

| Instruction               | Meaning                                                     |
| ------------------------- | ----------------------------------------------------------- |
| `FROM`                    | Selects the base image containing Python                    |
| `WORKDIR`                 | Sets `/app` as the working directory inside the image       |
| `COPY requirements.txt .` | Copies the dependency list into the image                   |
| `RUN pip install ...`     | Installs the required Python packages during image building |
| `COPY . .`                | Copies the application files into the image                 |
| `EXPOSE 5000`             | Documents the port the application listens on               |
| `CMD`                     | Specifies the default command when the container starts     |

### How Docker builds the application

Base image

Python 3.12 slim

Install dependencies

Flask

Copy application files

Python, HTML and CSS

Build the Docker image

flask-calculator

## 8. Create `.dockerignore`

Purpose: Prevents unnecessary files from being included in the Docker build context.

```
venv/
.git/
__pycache__/
*.pyc
.env
```

### Why use `.dockerignore`?

- Avoids copying the local virtual environment.
- Reduces unnecessary files sent to Docker.
- Excludes Git repository metadata.
- Helps prevent accidental inclusion of environment files containing secrets.

Never copy passwords, API keys, or other credentials into a Docker image.

## 9. Create the GitHub Actions Workflow

Create the following folder structure:

```
.github/
└── workflows/
    └── build.yml
```

Purpose: Automates code validation and Docker image building whenever the configured GitHub events occur.

### `build.yml`

```
name: Flask Calculator CI

on:
  push:
    branches:
      - main
      - dev

  pull_request:
    branches:
      - main

jobs:
  build:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout Code
        uses: actions/checkout@v4

      - name: Setup Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.12"

      - name: Install Dependencies
        run: python -m pip install -r requirements.txt

      - name: Validate Python File
        run: python -m py_compile app.py

      - name: Build Docker Image
        run: docker build -t flask-calculator .
```

### Explanation of the workflow

| Component              | Purpose                                                |
| ---------------------- | ------------------------------------------------------ |
| `name`                 | Gives the workflow a readable name                     |
| `on`                   | Defines which events trigger the workflow              |
| `push`                 | Runs when code is pushed to `main` or `dev`            |
| `pull_request`         | Runs when a pull request targets `main`                |
| `jobs`                 | Defines the work the workflow performs                 |
| `runs-on`              | Selects an Ubuntu runner provided by GitHub            |
| `actions/checkout`     | Downloads the repository's source code into the runner |
| `actions/setup-python` | Configures Python 3.12                                 |
| `pip install`          | Installs project dependencies                          |
| `py_compile`           | Checks the Python file for syntax errors               |
| `docker build`         | Builds the Docker image                                |

Important: `py_compile` validates syntax, not the complete application's behavior. A separate test suite would be needed to test the calculator's functionality. This workflow also does not push the image to Docker Hub or deploy it to AWS.

## 10. Run the Application Locally

Before using Docker or GitHub Actions, verify that the application works on your computer.

### Step 1: Open the project directory

```
cd calculator-app
```

### Step 2: Install dependencies

```
python -m pip install -r requirements.txt
```

### Step 3: Start the application

```
python app.py
```

### Step 4: Open the application

Open your browser and visit:

[http://localhost:5000](http://localhost:5000)

Try adding, subtracting, multiplying, and dividing numbers. Also test division by zero to confirm the error handling works.

Stop the development server with `Ctrl + C`.

Note: Flask's built-in server is suitable for local development and learning, not production deployment.

## 11. Build and Run Using Docker

First, ensure Docker Desktop is installed and running on your computer.

### Step 1: Build the image

Run this command from the project directory:

```
docker build -t flask-calculator .
```

Explanation:

- `docker build`: Builds a container image.
- `-t flask-calculator`: Assigns the image a name.
- `.`: Uses the current directory as the build context.

### Step 2: Check the image

```
docker images
```

Look for `flask-calculator` in the output.

### Step 3: Run the container

```
docker run -d --name calculator-container -p 5000:5000 flask-calculator
```

Explanation:

- `-d`: Runs the container in the background.
- `--name`: Assigns a container name.
- `-p 5000:5000`: Maps host port 5000 to container port 5000.
- `flask-calculator`: Specifies the image to run.

### Step 4: Access the calculator

Visit [http://localhost:5000](http://localhost:5000).

### Step 5: Check the running container

```
docker ps
```

### Step 6: View container logs

```
docker logs calculator-container
```

### Step 7: Stop and remove the container

```
docker stop calculator-container
docker rm calculator-container
```

## 12. Push the Project to GitHub

### Step 1: Create a GitHub repository

Create a new repository named `calculator-app` on GitHub. If you already have the files locally, creating the remote repository without a README or other initial files keeps the first push straightforward.

### Step 2: Initialize Git

Run these commands from the project directory:

```
git init
git checkout -b dev
git add .
git commit -m "Initial Flask Calculator"
```

### Step 3: Connect the remote repository

Replace `<your-username>` with your GitHub username.

```
git remote add origin https://github.com/<your-username>/calculator-app.git
```

### Step 4: Push the development branch

```
git push -u origin dev
```

### Step 5: Verify GitHub Actions

1. Open the repository on GitHub.
2. Select the Actions tab.
3. Open the `Flask Calculator CI` workflow run.
4. Check each step for success or failure.

Because `dev` is configured as a push trigger, pushing your code to that branch should start the workflow.

## 13. Understand the Complete CI Pipeline

Step 1: Developer commits and pushes code

Git records changes, and GitHub receives the updated source code.

Step 2: GitHub Actions starts a job

GitHub provisions an Ubuntu runner and checks out the repository.

Step 3: Install Python dependencies

The runner installs Flask from requirements.txt.

Step 4: Validate the Python code

Python checks app.py for syntax errors.

Step 5: Build the Docker image

Docker creates the image on the GitHub-hosted runner.

Step 6: Report the workflow status

A successful build confirms these steps completed without errors. A failure needs investigation.

### What happens if the build fails?

Check the failed step in GitHub Actions:

- Dependency installation failure: check `requirements.txt` and package compatibility.
- Python validation failure: inspect syntax and indentation in `app.py`.
- Docker build failure: check the Dockerfile, file names, and build context.
- Application failure when running: inspect `docker logs calculator-container`.

A successful CI run means the configured checks passed. It does not automatically guarantee that the application is bug-free.

## 14. Interview Preparation

### Project explanation

You can explain your project like this:

I developed a web-based calculator using Python and Flask. I used Git for version control and GitHub to host the source code. I containerized the application using Docker and created a GitHub Actions workflow to automate dependency installation, Python syntax validation, and Docker image building whenever code is pushed to the configured branches.

This project helped me understand the fundamentals of containerization, source code management, continuous integration, and automated build pipelines.

### Common interview questions

1\. What is Flask?

Flask is a lightweight Python web framework used to build web applications and APIs.

2\. What is Docker?

Docker is a platform for packaging applications and their dependencies into portable container images and running them in containers.

3\. What is the difference between a Docker image and a container?

- Image: The packaged template used to start an application.
- Container: A running or stopped instance created from an image.

4\. What is GitHub Actions?

GitHub Actions is an automation platform that runs workflows in response to events such as pushes and pull requests.

5\. What is CI/CD?

- CI, Continuous Integration, automates activities such as code checks and builds.
- CD can mean Continuous Delivery or Continuous Deployment, which extends the pipeline toward releasing or deploying software.

6\. Why use a Dockerfile?

It defines the repeatable instructions needed to build the application's Docker image.

7\. Why use `.dockerignore`?

It prevents unnecessary files from entering the build context and helps reduce the risk of including sensitive local files.

8\. Does this project deploy the application automatically?

No. The current workflow validates the code and builds the Docker image. Automatic deployment would require additional pipeline steps and a target environment.

## 15. Practical Checklist

Use this checklist to track your progress.

### Project progress

### 0/13

Create the project folders and files

Write app.py and understand Flask routes

Create the HTML template

Add CSS styling

Create requirements.txt and install Flask

Run the application locally

Build the Docker image

Run and inspect the Docker container

Create the GitHub repository

Push code to the dev branch

Configure and run GitHub Actions

Review a successful workflow run

Practice explaining the pipeline in an interview

Reset checklist

## 16. Next Steps: Turn This into a Full DevOps Project

Once this version works, you can expand it gradually:

| Level | Enhancement                                  | Skill learned          |
| ----- | -------------------------------------------- | ---------------------- |
| 1     | Add automated unit tests with `pytest`       | Testing                |
| 2     | Push the Docker image to Docker Hub          | Container registries   |
| 3     | Add image tagging and versioning             | Release management     |
| 4     | Deploy to an AWS EC2 instance                | Cloud deployment       |
| 5     | Automate deployment through GitHub Actions   | Continuous Delivery    |
| 6     | Add CloudWatch monitoring and logs           | Observability          |
| 7     | Provision AWS infrastructure using Terraform | Infrastructure as Code |

Recommended next milestone: Add `pytest` tests and make GitHub Actions run them before building the Docker image. That gives you a more meaningful CI pipeline: test first, build second, and deploy only after the required checks pass.
