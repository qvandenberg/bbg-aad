# User manual

Dash & CLI app to compute order prices for brass rods (a copper : zinc alloy). 

Manufacturing costs depend on the weight, rod length, the ratio of copper : zinc and their respective prices.

The calculation for order prices is done in a directed acyclic graph. Each of the order parameters is a node on the graph, and the computation is split into single assignment code. The benefit of this approach is that we can do the sensitivity analysis to price shocks all in one calculation. The price shock effects are evaluated through the partial derivatives computed in the node graph. This approximation becomes exact when the price model is linear (as it is here).

In short, a single graph traversal gives both the final output + sensitivity. 

# Run instructions
Ensure Docker and Docker Compose are installed on the system.

Create and run the Docker container with:
`docker-compose up`

Open an internet browser and navigate to http://127.0.0.1:7071/ (this is the local host)

## Enter parameters in the user interface
Before the price calculation, we need some parameters. Below data field can be changed if desired:

- Copper fraction slider
- Labour factor table
- Copper price
- Zinc prices
- Order parameters
- Sensitivity analysis price shock range

Press the `Calculate prices` button to compute the total price and sensitivity calculation. The sensitivity calculation uses algorithmic differentiation under the hood in the `pricing/ComputationalNode` and `pricing/DirectedAcyclicGraph` classes.

In the `/docs` folder there is a sample of what the front end should look like.

# Run unit tests
Ensure dependencies are installed and written to the poetry lock file by running `poetry install; poetry lock`

Run unit tests from the root folder through `poetry run pytest`