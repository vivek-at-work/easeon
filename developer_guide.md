# Developer Guide
## Development Environment Setup
### Prerequisites
    1. Ubuntu bionic 18.4
    2. Python 3.7.4
    3. Pipenv

### Step 1: Clone code from github repository
    git clone git@github.com:VivekDSrivastava/easeOn.git

### Step 2 :Setup Database
    cd easeOn/EaseOn/bin
    sudo chmod +x ./setup.sh
    ./setup.sh

### Step 3: Install Dependencies
    cd ../../
    pipenv install

### Step 4 :Setup Env Variables
easeOn Code base relies heavily on environment variables and it use django environ for managing its environment variables.

    cd EaseOn/settings
    vi .env





### Step 5 :Run database Migrations

### Step 6 :Load Initial Data
    python manage.py loaddata data

### Step 7 : Start the Development server
