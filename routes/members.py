from flask import Blueprint, request, jsonify
from database import db
from models import Member

members_bp = Blueprint('members', __name__)

@members_bp.route('/', methods=['GET'])
def get_members():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    members = Member.query.paginate(page=page, per_page=per_page, error_out=False)
    return jsonify({
        'members': [{'id': member.id, 'name': member.name, 'email': member.email} for member in members.items],
        'total': members.total,
        'pages': members.pages
    })

@members_bp.route('/', methods=['POST'])
def add_member():
    data = request.json
    if 'name' not in data or 'email' not in data:
        return jsonify({'message': 'Missing required fields'}), 400
    
    existing_member = Member.query.filter_by(email=data['email']).first()
    if existing_member:
        return jsonify({'message': 'Email already exists'}), 400
    
    new_member = Member(name=data['name'], email=data['email'])
    db.session.add(new_member)
    db.session.commit()
    return jsonify({'message': 'Member added successfully'}), 201

@members_bp.route('/<int:member_id>', methods=['PUT'])
def update_member(member_id):
    data = request.json
    member = Member.query.get(member_id)
    if not member:
        return jsonify({'message': 'Member not found'}), 404
    
    member.name = data.get('name', member.name)
    member.email = data.get('email', member.email)
    db.session.commit()
    return jsonify({'message': 'Member updated successfully'})

@members_bp.route('/<int:member_id>', methods=['DELETE'])
def delete_member(member_id):
    member = Member.query.get(member_id)
    if not member:
        return jsonify({'message': 'Member not found'}), 404
    
    db.session.delete(member)
    db.session.commit()
    return jsonify({'message': 'Member deleted successfully'})

@members_bp.route('/search', methods=['GET'])
def search_members():
    query = request.args.get('q')
    members = Member.query.filter(
        (Member.name.ilike(f'%{query}%')) | (Member.email.ilike(f'%{query}%'))
    ).all()
    return jsonify([{'id': member.id, 'name': member.name, 'email': member.email} for member in members])
