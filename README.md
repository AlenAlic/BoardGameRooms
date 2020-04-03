# BoardGameRooms
> Realtime webapp to play online (board)games in separate rooms.



## Contribute
You can contribute to this project by adding games to it's library.

Click [here][CONTRIBUTE] to see the details on the requirements and other details.



## Development
Made with Flask backend and Vue frontend.
#### Install dependencies
    # create venv
    python3 -m venv venv
    source venv/bin/activate
    
    # install dependencies
    pip install -r requirements.txt
    npm install
#### Dev servers
    # frontend
    npm run serve
    
    # backend (Werkzeug)
    flask run
    # backend (eventlet)
    python3 run.py



## Production
### Preparations
Before installing, make sure you have a domain name available.
#### Installing the application
Install the application through git:

    git clone https://github.com/AlenAlic/BoardGameRooms
    cd BoardGameRooms
### Variables
Before installing anything, set the following environment variables:

    export FLASK_APP=run.py
    export DOMAIN=<domain_url>

Run the `deployment/deploy.sh` script.




[CONTRIBUTE]: ./CONTRIBUTE.md
