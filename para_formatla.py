
import locale

def standart_formatla(para):

    currency = "${:,.2f}".format(para)

    return currency

def locale_turkish_formatla(para):

    locale.setlocale(locale.LC_ALL, "tr_TR.utf8")

    return locale.currency(para, grouping=True)


def turkish_formatla(para):
    binlik_ayrac = "."
    ondalik_ayrac = ","

    currency = "{:,.2f}".format(para)

    if binlik_ayrac == '.':
        tamsayi_kisim = currency.split('.')[0]
        ondalik_kisim = currency.split('.')[1]

        yeni_tamsayi_kisim = tamsayi_kisim.replace(',', '.')
        currency = yeni_tamsayi_kisim + ondalik_ayrac + ondalik_kisim + " TL"
    else:
        currency = '$' + currency

    return currency


print(standart_formatla(123456789.45))
print(turkish_formatla(123456789.45))
print(locale_turkish_formatla(123456789.45))

