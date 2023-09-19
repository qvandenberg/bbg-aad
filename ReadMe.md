# User manual

Dash app to compute order prices for brass rods (a copper : zinc alloy). 

Client pricing depends on the weight, rod length, the ratio of copper : zinc and their respective material prices.

The calculation for order prices is performed in a directed acyclic graph. Each of the order parameters represents a node on the graph, and the computation is split into single assignment code. The benefit of this approach is that we obtain the order price as well as its derivative w.r.t. each input parameter. This allows us to do a sensitivity analysis to see the effect of price shocks of the raw materials on the final order price without repeating the original calculation. The price shock effects are evaluated through the partial derivatives computed in the node graph. This approximation becomes exact when the price model is linear (as it is here).

In short, a single graph traversal yields both the final price output + sensitivity. 

# Run instructions
Ensure Docker and Docker Compose are installed on the system.

Create and run the Docker container with:
`docker-compose up aad-pricing --build`

Open an internet browser and navigate to http://127.0.0.1:7071/ to see the UI on the local host.
<img src="/docs/ui-example.png" alt="UI sample">

Run unit tests with:
`docker-compose up -d aad-pricing-tests`
`docker run -it --rm -v ${PWD}:/testRunner -v ${PWD}/reports/allure:/testRunner/allure docker-test:latest poetry run pytest --junitxml=reports/allure/test-results.xml`
Test results are exported to:
`/reports/allure/`

## Manual steps to build with poetry
From `root`:

rm -r dist; pip uninstall aad_pricing; poetry build --format wheel; pip install dist/*; python applications/server.py

## Enter parameters in the user interface
Before the price calculation, we need some parameters. Below data field can be changed if desired:

- Copper fraction slider
- Labour factor table
- Copper price
- Zinc prices
- Order parameters (weight, rod length, zinc quality)
- Sensitivity analysis price shock range

Press the `Calculate prices` button to compute the total price and sensitivity calculation. The sensitivity calculation uses algorithmic differentiation under the hood in the `pricing/ComputationalNode` and `pricing/DirectedAcyclicGraph` classes.

# Run unit tests
Ensure dependencies are installed and written to the poetry lock file by running `poetry install; poetry lock`

Run unit tests from the root folder through `poetry run pytest`

## Acknowledgement
Favicon created by Surang:
<a href="https://www.flaticon.com/free-icons/metal" title="metal icons">Metal icons created by surang - Flaticon</a>
