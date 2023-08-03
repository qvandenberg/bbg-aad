# User manual

Dash & CLI app to compute order prices for brass rods (a copper : zinc alloy). 

Manufacturing costs depend on the weight, rod length, the ratio of copper : zinc and their respective prices.

The calculation for order prices is done in a directed acyclic graph. Each of the order parameters is a node on the graph, and the computation is split into single assignment code. The benefit of this approach is that we can do the sensitivity analysis to price shocks all in one calculation. The price shock effects are evaluated through the partial derivatives computed in the node graph. This approximation becomes exact when the price model is linear (as it is here).

In short, a single graph traversal gives both the final output + sensitivity. 

# Get started
Create a virtual environment with python version 3.8 or above and install the dependencies. 

Pip: run `pip install -r requirements.txt`
Conda (create environment directly from the requirements file): run `conda create --name <env> --file conda-requirements.txt` 

## Run example script with main application
navigate to the `src` folder. From there, run `python main.py` to run the example in the pdf assignment. It can be tweaked beforehand to run with different values.

## Run front end in Dash app
Start the dash app by running `python dash_app.py` from the `src` folder. Open a browser and navigate to 'http://127.0.0.1:10453/' to operate the application in the UI (or localhost:10453). 

There is little input validation in the front end, but it should be self-explanatory.

Data fields that can be changed:
- Copper fraction slider
- Labour factor table
- Copper price
- Zinc prices
- Order parameters
- Sensitivity analysis shock ladders

In the `/docs` folder there is a sample of what the front end should look like.