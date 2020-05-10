def find(user_id, session, User):
    query_user = session.query(User).filter(User.id == user_id).first()
    if query_user:
        query_ath_height = session.execute('select name, height from athelete where abs( height - {0} ) = ( select min( abs( height - {0} ) ) from athelete ) order by name limit 1'.format(query_user.height))
        query_ath_birthdate = session.execute('select name, birthdate from athelete where abs( strftime( "%s", birthdate ) - strftime( "%s", "{0}" ) ) = ( select min( abs( strftime( "%s", birthdate ) - strftime( "%s", "{0}" ) ) ) from athelete ) order by name limit 1'.format(query_user.birthdate))
        return query_ath_height, query_ath_birthdate
    else: print('Нет такого пользователя')
    return None, None