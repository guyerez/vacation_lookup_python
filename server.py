import os
from datetime import date, datetime

from flask import Flask, jsonify, request

from database import count_vacations, get_vacation, init_database, list_vacations, set_vacation

app = Flask(__name__)


@app.route('/vacation', methods=['POST'])
def post_vacation():
    body = request.get_json(silent=True) or {}
    username = body.get('username')
    vacation_date = body.get('date')

    if not username or not vacation_date:
        return jsonify({'error': 'Username and date are required'}), 400

    try:
        set_vacation(username, vacation_date)
        return jsonify({'success': True, 'message': f'Vacation set for {username} on {vacation_date}'})
    except Exception as error:
        return jsonify({'error': str(error)}), 500


@app.route('/vacation/<username>', methods=['GET'])
def get_vacation_status(username):
    if not username:
        return jsonify({'error': 'Username is required'}), 400

    try:
        vacation_date_str = get_vacation(username)

        if vacation_date_str:
            vacation_date = datetime.fromisoformat(vacation_date_str).date()
            is_on_vacation = vacation_date == date.today()
            return jsonify({
                'username': username,
                'onVacation': 'yes' if is_on_vacation else 'no',
                'vacationDate': vacation_date_str,
            })
        else:
            return jsonify({'username': username, 'onVacation': 'no'})
    except Exception as error:
        return jsonify({'error': str(error)}), 500


@app.route('/vacations', methods=['GET'])
def get_vacations():
    sort = request.args.get('sort', 'username')

    try:
        return jsonify(list_vacations(sort))
    except Exception as error:
        return jsonify({'error': str(error)}), 500


@app.route('/vacations/count', methods=['GET'])
def get_vacations_count():
    group = request.args.get('group', 'vacation_date')

    try:
        return jsonify(count_vacations(group))
    except Exception as error:
        return jsonify({'error': str(error)}), 500


def start_server():
    port = int(os.environ.get('PORT', 3000))
    print(f'Vacation Lookup API running on port {port}')
    app.run(host='0.0.0.0', port=port)


if __name__ == '__main__':
    init_database()
    start_server()
