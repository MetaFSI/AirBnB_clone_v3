#!/usr/bin/python3
"""
Create a new view for State objects - handles all default RESTful API actions.
"""

# Import necessary modules
from flask import abort, jsonify, request
from models.state import State
from api.v1.views import app_views
from models import storage

# Route for retrieving all State objects


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def get_all_states():
    """
    Retrieves list of all State objects.
    """
    # Get all State objects from storage
    states = storage.all(State).values()
    # Convert objects to dictionaries and jsonify list
    state_list = [state.to_dict() for state in states]
    return jsonify(state_list)

# Route for retrieving a specific State object by ID


@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def get_state(state_id):
    """
    Retrieves a State object.
    """
    # Get State object with given ID from storage
    state = storage.get(State, state_id)
    if state:
        # Return State object in JSON format
        return jsonify(state.to_dict())
    else:
        # Return 404 error if State object is not found
        abort(404)

# Route for deleting a specific State object by ID


@app_views.route('/states/<state_id>', methods=['DELETE'])
def delete_state(state_id):
    """
    Deletes a State object.
    """
    # Get State object with given ID from storage
    state = storage.get(State, state_id)
    if state:
        # Delete State object from storage and save changes
        storage.delete(state)
        storage.save()
        # Return an empty JSON with 200 status code
        return jsonify({}), 200
    else:
        # Return 404 error if State object is not found
        abort(404)

# Route for creating a new State object


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def create_state():
    """
    Creates a State object.
    """
    if not request.get_json():
        # Return 400 error if request data is not in JSON format
        abort(400, 'Not a JSON')

    # Get JSON data from request
    kwargs = request.get_json()
    if 'name' not in kwargs:
        # Return 400 error if 'name' key is missing in JSON data
        abort(400, 'Missing name')

    # Create a new State object with JSON data
    state = State(**kwargs)
    # Save State object to storage
    state.save()
    # Return newly created State object in JSON format with 201 status code
    return jsonify(state.to_dict()), 201

# Route for updating an existing State object by ID


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def update_state(state_id):
    """
    Updates a State object.
    """
    # Get State object with given ID from storage
    state = storage.get(State, state_id)
    if state:
        if not request.get_json():
            # Return 400 error if request data is not in JSON format
            abort(400, 'Not a JSON')

        # Get JSON data from request
        data = request.get_json()
        ignore_keys = ['id', 'created_at', 'updated_at']
        # Update attributes of State object with JSON data
        for key, value in data.items():
            if key not in ignore_keys:
                setattr(state, key, value)

        # Save updated State object to storage
        state.save()
        # Return updated State object in JSON format with 200 status code
        return jsonify(state.to_dict()), 200
    else:
        # Return 404 error if State object is not found
        abort(404)

# Error Handlers:


@app_views.errorhandler(404)
def not_found(error):
    """
    Raises a 404 error.
    """
    # Return a JSON response for 404 error
    response = {'error': 'Not found'}
    return jsonify(response), 404


@app_views.errorhandler(400)
def bad_request(error):
    """
    Returns a Bad Request message for illegal requests to API.
    """
    # Return a JSON response for 400 error
    response = {'error': 'Bad Request'}
    return jsonify(response), 400
