from flask import Flask, request, jsonify
from flask_cors import CORS
from services.asset_management import AssetProcessor, AssetManager, AssetService
import os
import logging

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable Cross-Origin Resource Sharing (CORS) for all routes

# Initialize logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("app.log"),  # Log to a file
        logging.StreamHandler(),  # Log to the console
    ],
)

# Set up the directory where asset JSON files are stored
script_dir = os.path.dirname(os.path.abspath(__file__))
assets_dir = os.path.join(script_dir, "assets")

# Initialize AssetProcessor with the directory containing JSON files
asset_processor = AssetProcessor(assets_dir)

# Initialize AssetManager with AssetProcessor
asset_manager = AssetManager(asset_processor)

# Initialize the Service Layer with AssetManager
asset_service = AssetService(asset_manager)


# Routes
@app.route("/assets", methods=["GET"])
def get_assets():
    """
    Fetch a paginated list of assets from the JSON files.

    Query Parameters:
        page (int, optional): Page number for pagination (default is 1).
        per_page (int, optional): Number of items per page (default is 5).

    Returns:
        JSON response with the list of assets and pagination details:
            - assets: List of assets on the current page.
            - total: Total number of assets available.
            - page: Current page number.
            - per_page: Number of assets per page.
    """
    try:
        page = int(request.args.get("page", 1))  # Default to page 1 if not provided
        per_page = int(request.args.get("per_page", 5))  # Default to 5 items per page

        logging.info(
            f"Received request to fetch assets: page={page}, per_page={per_page}"
        )
        assets_data = asset_service.get_paginated_assets(page=page, per_page=per_page)
        return jsonify(assets_data)
    except Exception as e:
        logging.error(f"An error occurred while fetching assets: {e}")
        return jsonify({"message": "Error fetching assets"}), 500


@app.route("/match", methods=["POST"])
def match_asset():
    """
    Match an asset based on a search query that can be a part of the name, model, or IP address.

    Request Body (JSON):
        search (str): The search query to match against asset fields.

    Returns:
        JSON response with the matched asset data or a message indicating no match:
            - IP Address, Model, Name: Details of the matched asset.
            - message: 'No Asset Found' if no match is found.
    """
    data = request.json
    search_query = data.get("search", "")
    logging.info(f"Received search request with query: {search_query}")
    try:
        return jsonify(asset_service.find_asset_by_query(search_query))
    except Exception as e:
        logging.error(f"An error occurred during the search request: {e}")
        return jsonify({"message": "Error during search"}), 500


if __name__ == "__main__":
    app.run(debug=True)
