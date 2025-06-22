from sqlalchemy.orm import Session
from collections import defaultdict
from app.models import Group, Expense, User


def calculate_balances(group_id: int, db: Session) -> list[dict]:
    # Pobierz grupę z użytkownikami i wydatkami
    group = db.query(Group).filter(Group.id == group_id).first()

    if not group:
        raise ValueError("Group not found")

    users = group.users
    expenses = db.query(Expense).filter(Expense.group_id == group_id).all()
    user_ids = [u.id for u in users]
    num_users = len(users)


    print(f"Calculating balances for group {group_id} named {group.name} with {users} users and {len(expenses)} expenses")
    if num_users < 2:
        return []

    # Slownik: kto komu ile jest winien
    raw_balances = defaultdict(lambda: defaultdict(float))  # raw_balances[debtor][creditor] = kwota

    for expense in expenses:
        if expense.user_id not in user_ids:
            continue  # ktoś spoza grupy – ignoruj

        per_user_share = expense.amount / num_users

        for user in users:
            if user.id == expense.user_id:
                continue  # ten kto płacił nie jest sobie winien
            raw_balances[user.id][expense.user_id] += per_user_share

    # Redukujemy wzajemne długi
    final_balances = []

    for u1 in user_ids:
        for u2 in user_ids:
            if u1 == u2:
                continue
            owes = raw_balances[u1][u2]
            owed_back = raw_balances[u2][u1]
            net = round(owes - owed_back, 2)
            if net > 0:
                final_balances.append({
                    "debtor_id": u1,
                    "debtor_username" : db.query(User).filter(User.id == u1).first().username,
                    "debtee_id": u2,
                    "debtee_username" : db.query(User).filter(User.id == u2).first().username,
                    "amount": net
                })
    for user in raw_balances:
        print(raw_balances[user])

    return final_balances

