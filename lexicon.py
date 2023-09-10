class LexiconRU:
    def stats_message(self, users):
        return '<b>Статистика на данный момент: </b> \n\n' \
               f'Зарегистрировано в боте: {users} человек'

lexicon = LexiconRU()