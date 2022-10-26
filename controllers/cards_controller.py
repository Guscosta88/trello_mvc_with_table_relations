from flask import Blueprint, request
from init import db
from datetime import date
from models.card import Card, CardSchema
from controllers.auth_controller import authorize
from flask_jwt_extended import jwt_required, get_jwt_identity



cards_bp = Blueprint('cards', __name__, url_prefix='/cards')


@cards_bp.route('/')
# @jwt_required()
def all_cards():
    #to test
    # return 'all_cards route'

    # if not authorize():
    #     return {'error': 'You must be an admin'}, 401
    stmt = db.select(Card).order_by(Card.priority.desc(), Card.title)
    cards = db.session.scalars(stmt)
    return CardSchema(many=True).dump(cards)

@cards_bp.route('/<int:id>/')
def one_card(id):
    stmt = db.select(Card).filter_by(id=id)
    card = db.session.scalar(stmt)
    if card:
        return CardSchema().dump(card)
    else:
        return {'error': f'Card not found with id {id}'}, 404

@cards_bp.route('/<int:id>/', methods=['DELETE'])
@jwt_required()
def delete_one_card(id):
    authorize()

    stmt = db.select(Card).filter_by(id=id)
    card = db.session.scalar(stmt)
    if card:
        db.session.delete(card)
        db.session.commit()
        return {'message': f'Card "{card.title}" deleted successfully'}
    else:
        return {'error': f'Card not found with id {id}'}, 404

@cards_bp.route('/<int:id>/', methods=['PUT', 'PATCH'])
@jwt_required()
def update_one_card(id):
    stmt = db.select(Card).filter_by(id=id)
    card = db.session.scalar(stmt)
    if card:
        card.title = request.json.get('title') or card.title
        card.description = request.json.get('description') or card.description
        card.status = request.json.get('status') or card.status
        card.priority = request.json.get('priority') or card.priority
        db.session.commit()
        return CardSchema().dump(card)
    else:
        return {'error': f'Card not found with id {id}'}, 404

@cards_bp.route('/', methods=['POST'])
@jwt_required()
def create_card():
        card = Card(
            title = request.json['title'],
            description = request.json['description'],
            date = date.today(),
            status = request.json['status'],
            priority = request.json['priority'],
            user_id = get_jwt_identity()
        )

        db.session.add(card)
        db.session.commit()

        return CardSchema().dump(card), 201
