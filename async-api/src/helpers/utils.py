def errorWarning(value, message: str, itemId: str | None) -> str:
    """
    функция возвращает сообщение пользователю в случае неуспешного поиска
    :param value: film(s), genre(s), person(s) (мб любое значение, в рамках задачи передаются перечисленные)
    :param message: какое сообщение вернуть (сделать параметр целочисленным интуитивно непонятно при вызове функции)
    :param itemId: нужен в случае, когда поиск осуществляется по id
    :return:
    """
    if message == 'nf':
        return f'{value} not found'
    elif message == 'notInES':
        valueId = f'(id: {itemId})' if itemId else ''
        return f'An error occurred while trying to find {value} in ES {valueId}'
