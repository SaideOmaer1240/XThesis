from datetime import datetime
class DateTime:
    def get_month():
            current_month = datetime.now().month    
            months = {
                1 : 'Janeiro',
                2 : 'Fevereiro',
                3 : 'Março',
                4 : 'Abril',
                5 : 'Maio',
                6 : 'Junho',
                7 : 'Julho',
                8 : 'Agosto',
                9 : 'Setembro',
                10 : 'Outubro',
                11 : 'Novembro',
                12 : 'Dezembro',
            }
            return months.get(current_month)
    def year():
        year = datetime.now().year 
        return year