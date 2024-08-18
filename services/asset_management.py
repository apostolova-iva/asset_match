import os
import json
import logging

class AssetProcessor:
    """
    AssetProcessor is responsible for handling the processing of asset files.
    It manages the listing, reading, and extracting of asset information from JSON files.
    """

    def __init__(self, directory):
        """
        Initializes AssetProcessor with a directory containing asset JSON files.

        Args:
            directory (str): The path to the directory containing the JSON files.
        """
        self.directory = directory
        logging.info(f"AssetProcessor initialized with directory: {self.directory}")

    def list_json_files(self):
        """
        Lists all JSON files in the specified directory.

        Returns:
            list: A list of file paths to JSON files in the directory.
        """
        try:
            files = [os.path.join(self.directory, filename) for filename in os.listdir(self.directory)
                     if filename.endswith('.json')]
            logging.info(f"Found {len(files)} JSON files in directory: {self.directory}")
            return files
        except FileNotFoundError:
            logging.error(f"Directory not found: {self.directory}. Please ensure the directory exists.")
            return []
        except PermissionError:
            logging.error(f"Permission denied for directory: {self.directory}. Check directory permissions.")
            return []
        except Exception as e:
            logging.error(f"An unexpected error occurred while accessing the directory: {self.directory}. Error: {e}")
            return []

    def read_json_file(self, file_path):
        """
        Reads a JSON file and yields each asset one by one.

        Args:
            file_path (str): The path to the JSON file.

        Yields:
            dict: A dictionary representing asset information extracted from the JSON file.
        """
        try:
            with open(file_path, 'r') as file:
                logging.info(f"Reading JSON file: {file_path}")
                data = json.load(file)

                if isinstance(data, dict) and 'assets' in data:
                    assets = data['assets']
                elif isinstance(data, list):
                    assets = data
                else:
                    raise ValueError(f"Unexpected data format in file {file_path}")

                # Yield each asset individually
                for asset in assets:
                    yield asset

        except FileNotFoundError:
            logging.error(f"File not found: {file_path}. Please ensure the file exists.")
        except PermissionError:
            logging.error(f"Permission denied for file: {file_path}. Check file permissions.")
        except json.JSONDecodeError as e:
            logging.error(f"Error decoding JSON in file {file_path}: {e}")
        except Exception as e:
            logging.error(f"An unexpected error occurred while reading the file {file_path}: {e}")

    def extract_asset_info(self, asset):
        """
        Extracts the 'name', 'model', and 'ip address' from a single asset dictionary.

        Args:
            asset (dict): A dictionary representing an asset.

        Returns:
            dict or None: A dictionary with 'Name', 'Model', and 'IP Address' if all fields are found, otherwise None.
        """
        try:
            name = asset.get('name') or asset.get('name_snmp') or asset.get('asset-name')
            model = asset.get('model') or asset.get('asset-model')
            ip_address = asset.get('ip_address') or asset.get('ipv4') or asset.get('ip-address')

            if name and model and ip_address:
                logging.debug(f"Asset extracted: Name={name}, Model={model}, IP Address={ip_address}")
                return {
                    'Name': name,
                    'Model': model,
                    'IP Address': ip_address
                }
            else:
                logging.debug(f"Asset skipped due to missing fields: {asset}")
                return None
        except Exception as e:
            logging.error(f"An error occurred while extracting asset information. Error: {e}")
            return None


class AssetManager:
    """
    AssetManager is responsible for managing the collection and pagination of assets.
    It interacts with the AssetProcessor to gather and process asset data.
    """

    def __init__(self, asset_processor):
        """
        Initializes AssetManager with an AssetProcessor instance.

        Args:
            asset_processor (AssetProcessor): The processor to handle asset data.
        """
        self.asset_processor = asset_processor
        logging.info("AssetManager initialized")

    def collect_all_assets(self):
        """
        Collects all assets from the JSON files.

        Returns:
            list: A list of all extracted assets.
        """
        all_assets = []
        try:
            json_files = self.asset_processor.list_json_files()
            logging.info(f"Starting to collect assets from {len(json_files)} JSON files")

            for file_path in json_files:
                for asset in self.asset_processor.read_json_file(file_path):
                    extracted_asset = self.asset_processor.extract_asset_info(asset)
                    if extracted_asset:
                        all_assets.append(extracted_asset)
                        # Log every 5 assets to avoid excessive logging
                        if len(all_assets) % 5 == 0:
                            logging.debug(f"Collected {len(all_assets)} assets so far...")

        except ValueError as ve:
            logging.error(f"Skipping file {file_path} due to a data format error: {ve}")
        except Exception as e:
            logging.error(f"An unexpected error occurred while collecting assets: {e}")

        logging.info(f"Total assets collected: {len(all_assets)}")
        return all_assets

    def collect_assets_paginated(self, page=1, per_page=5):
        """
        Collects assets with pagination.

        Args:
            page (int): The page number.
            per_page (int): The number of assets per page.

        Returns:
            dict: A dictionary containing paginated assets and metadata including total count.
        """
        all_assets = self.collect_all_assets()
        start = (page - 1) * per_page
        end = start + per_page
        paginated_assets = all_assets[start:end]

        logging.info(f"Returning {len(paginated_assets)} assets for page {page} with {per_page} per page")
        return {
            'assets': paginated_assets,
            'total': len(all_assets),
            'page': page,
            'per_page': per_page
        }

    def match_asset(self, search_query):
        """
        Matches an asset based on a search query that can be part of the name, model, or IP address.

        Args:
            search_query (str): The search query to match against asset fields.

        Returns:
            dict: The matched asset data or a message indicating no match.
        """
        search_query = search_query.lower()
        logging.info(f"Searching for asset matching query: {search_query}")

        try:
            for file_path in self.asset_processor.list_json_files():
                for asset in self.asset_processor.read_json_file(file_path):
                    extracted_asset = self.asset_processor.extract_asset_info(asset)
                    if extracted_asset:
                        # Check if the search query matches any of the fields
                        if (search_query in extracted_asset['IP Address'].lower() or
                            search_query in extracted_asset['Model'].lower() or
                            search_query in extracted_asset['Name'].lower()):
                            logging.info(f"Match found for query '{search_query}': {extracted_asset}")
                            return extracted_asset  # Return the first matched asset

            logging.info(f"No match found for query: {search_query}")
            return {'message': 'No Asset Found'}  # No matches found
        except ValueError as ve:
            logging.error(f"Skipping file {file_path} due to a data format error: {ve}")
        except Exception as e:
            logging.error(f"An error occurred during asset matching. Error: {e}")
            return {'message': 'Error during search'}


class AssetService:
    """
    AssetService provides a service layer to manage asset operations such as pagination and searching.
    It acts as a bridge between the AssetManager and the application logic.
    """

    def __init__(self, asset_manager):
        """
        Initializes AssetService with an AssetManager instance.

        Args:
            asset_manager (AssetManager): The manager to handle asset operations.
        """
        self.asset_manager = asset_manager
        logging.info("AssetService initialized")

    def get_paginated_assets(self, page, per_page):
        """
        Fetches paginated assets.

        Args:
            page (int): The page number.
            per_page (int): The number of assets per page.

        Returns:
            dict: A dictionary containing paginated assets data.
        """
        try:
            logging.info(f"Fetching paginated assets: page={page}, per_page={per_page}")
            return self.asset_manager.collect_assets_paginated(page=page, per_page=per_page)
        except Exception as e:
            logging.error(f"Error in service layer during pagination: {e}")
            return {'message': 'Error fetching assets'}

    def find_asset_by_query(self, search_query):
        """
        Finds an asset by a search query.

        Args:
            search_query (str): The search query to match against asset fields.

        Returns:
            dict: Matched asset data or a message indicating no match.
        """
        try:
            logging.info(f"Finding asset by query: {search_query}")
            return self.asset_manager.match_asset(search_query)
        except Exception as e:
            logging.error(f"Error in service layer during search: {e}")
            return {'message': 'Error during search'}
