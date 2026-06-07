from flask import Blueprint, jsonify, redirect, render_template, request, url_for
from sqlalchemy import or_
from flask_login import login_required
from sqlalchemy.exc import SQLAlchemyError

from app import db
from app.models.supplier import Supplier

supplier_bp = Blueprint('supplier', __name__)


def _supplier_payload(supplier):
    return {
        'id': supplier.id,
        'name': supplier.name,
        'contact_person': supplier.contact_person,
        'phone': supplier.phone,
        'email': supplier.email,
        'address': supplier.address,
    }


def _supplier_form_data():
    data = request.get_json(silent=True) if request.is_json else request.form
    data = data or {}

    return {
        'name': (data.get('name') or '').strip(),
        'contact_person': (data.get('contact_person') or '').strip() or None,
        'phone': (data.get('phone') or '').strip() or None,
        'email': (data.get('email') or '').strip() or None,
        'address': (data.get('address') or '').strip() or None,
    }


def _wants_json():
    return request.is_json or request.accept_mimetypes.best == 'application/json'


@supplier_bp.route('/')
@login_required
def index():
    search = request.args.get('search', '').strip()
    query = Supplier.query

    if search:
        like_search = f'%{search}%'
        query = query.filter(
            or_(
                Supplier.name.ilike(like_search),
                Supplier.contact_person.ilike(like_search),
                Supplier.phone.ilike(like_search),
                Supplier.email.ilike(like_search),
            )
        )

    suppliers = query.order_by(Supplier.name.asc()).all()
    return render_template('suppliers.html', suppliers=suppliers)


@supplier_bp.route('/api')
@login_required
def api_suppliers():
    search = request.args.get('search', '').strip()
    query = Supplier.query

    if search:
        like_search = f'%{search}%'
        query = query.filter(
            or_(
                Supplier.name.ilike(like_search),
                Supplier.contact_person.ilike(like_search),
                Supplier.phone.ilike(like_search),
                Supplier.email.ilike(like_search),
            )
        )

    suppliers = query.order_by(Supplier.name.asc()).all()
    return jsonify({
        'success': True,
        'suppliers': [_supplier_payload(supplier) for supplier in suppliers],
    })


@supplier_bp.route('/api/<int:supplier_id>')
@login_required
def api_supplier_detail(supplier_id):
    supplier = Supplier.query.get_or_404(supplier_id)
    return jsonify({
        'success': True,
        'supplier': _supplier_payload(supplier),
    })


@supplier_bp.route('/add', methods=['GET', 'POST'])
@supplier_bp.route('/api', methods=['POST'])
@login_required
def add_supplier():
    if request.method == 'GET':
        return render_template('add_supplier.html')

    data = _supplier_form_data()

    if not data['name']:
        if _wants_json():
            return jsonify({'success': False, 'message': 'Supplier name is required.'}), 400
        return redirect(url_for('supplier.index'))

    supplier = Supplier(**data)

    try:
        db.session.add(supplier)
        db.session.commit()
    except SQLAlchemyError:
        db.session.rollback()
        if _wants_json():
            return jsonify({'success': False, 'message': 'Unable to add supplier.'}), 500
        return redirect(url_for('supplier.index'))

    if _wants_json():
        return jsonify({
            'success': True,
            'message': 'Supplier added successfully.',
            'supplier': _supplier_payload(supplier),
        }), 201

    return redirect(url_for('supplier.index'))


@supplier_bp.route('/<int:supplier_id>/edit', methods=['POST'])
@supplier_bp.route('/api/<int:supplier_id>', methods=['PUT', 'PATCH'])
@login_required
def update_supplier(supplier_id):
    supplier = Supplier.query.get_or_404(supplier_id)
    data = _supplier_form_data()

    if not data['name']:
        if _wants_json():
            return jsonify({'success': False, 'message': 'Supplier name is required.'}), 400
        return redirect(url_for('supplier.index'))

    supplier.name = data['name']
    supplier.contact_person = data['contact_person']
    supplier.phone = data['phone']
    supplier.email = data['email']
    supplier.address = data['address']

    try:
        db.session.commit()
    except SQLAlchemyError:
        db.session.rollback()
        if _wants_json():
            return jsonify({'success': False, 'message': 'Unable to update supplier.'}), 500
        return redirect(url_for('supplier.index'))

    if _wants_json():
        return jsonify({
            'success': True,
            'message': 'Supplier updated successfully.',
            'supplier': _supplier_payload(supplier),
        })

    return redirect(url_for('supplier.index'))


@supplier_bp.route('/<int:supplier_id>/delete', methods=['POST'])
@supplier_bp.route('/api/<int:supplier_id>', methods=['DELETE'])
@login_required
def delete_supplier(supplier_id):
    supplier = Supplier.query.get_or_404(supplier_id)

    try:
        db.session.delete(supplier)
        db.session.commit()
    except SQLAlchemyError:
        db.session.rollback()
        if _wants_json():
            return jsonify({'success': False, 'message': 'Unable to delete supplier.'}), 500
        return redirect(url_for('supplier.index'))

    if _wants_json():
        return jsonify({
            'success': True,
            'message': 'Supplier deleted successfully.',
        })

    return redirect(url_for('supplier.index'))

