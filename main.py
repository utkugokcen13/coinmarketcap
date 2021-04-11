import requests
import json
from tkinter import *
from tkinter import messagebox, Menu
import sqlite3

con = sqlite3.connect('coin.db')
cursor = con.cursor()

def db_doldur():
    # Tabloyu düşürüyoruz.
    #cursor.execute("DROP TABLE coin")
    #con.commit()

    # Tabloyu oluşturuyoruz (Yoksa)
    cursor.execute("CREATE TABLE IF NOT EXISTS coin(id INTEGER PRIMARY KEY, symbol TEXT, "
                   "amount INTEGER, price REAL)")
    con.commit()

    cursor.execute("delete from coin")
    con.commit()

    cursor.execute("insert into coin values (1, 'BTC', 3, 45000)")
    con.commit()

    cursor.execute("insert into coin values (?,?,?,?)", (2, 'ADA', 300, 1.20))
    con.commit()

    cursor.execute("insert into coin values (3, 'LTC', 48, 185)")
    con.commit()

def insert_coin():
    cursor.execute("INSERT INTO coin values(?,?,?,?)",(portfolio_id_text.get(),
                                                       symbol_text.get(),
                                                       amount_text.get(),
                                                       price_text.get()))
    con.commit()
    messagebox.showinfo("Add Coin", symbol_text.get() + " added successfully")
    new_line_clear()
    ekran_temizle()

def update_coin():
    cursor.execute("UPDATE COIN set symbol=?, amount=?, price=? where id=?",(
                                                       symbol_text.get(),
                                                       amount_text.get(),
                                                       price_text.get(),
                                                       portfolio_id_text.get()))
    con.commit()
    messagebox.showinfo("Update Coin", symbol_text.get() + " updated successfully")
    new_line_clear()
    ekran_temizle()

def delete_coin():
    cursor.execute("DELETE FROM coin WHERE id=?", (portfolio_id_text.get(),))
    con.commit()
    messagebox.showinfo("Delete Coin", portfolio_id_text.get() + " deleted successfully")
    new_line_clear()
    ekran_temizle()

def new_line_clear():
    portfolio_id_text.set("")
    symbol_text.set("")
    amount_text.set("")
    price_text.set("")


def ekran_temizle():
    pencereler = window.winfo_children()

    for pencere in pencereler:
        pencere.destroy()

    app_menu()
    app_header()
    my_portfolio()

def rgb_color(rgb):
    return '#%02x%02x%02x' % rgb

def font_color_pl(para):
    if para > 0:
        return "green"
    elif para == 0:
        return "grey"
    else:
        return "red"


def turkish_formatla(para):
    binlik_ayrac = ","
    ondalik_ayrac = "."

    currency = "{:,.2f}".format(para)

    if binlik_ayrac == '.':
        tamsayi_kisim = currency.split('.')[0]
        ondalik_kisim = currency.split('.')[1]

        yeni_tamsayi_kisim = tamsayi_kisim.replace(',', '.')
        currency = yeni_tamsayi_kisim + ondalik_ayrac + ondalik_kisim + " TL"
    else:
        currency = '$' + currency

    return currency


def center_window(w=300, h=200):
    # get screen width and height
    ws = window.winfo_screenwidth()
    hs = window.winfo_screenheight()
    # calculate position x, y
    x = (ws / 2) - (w / 2)
    y = (hs / 2) - (h / 2)
    window.geometry('%dx%d+%d+%d' % (w, h, x, y))


def app_menu():
    def clear_portfolio():
        cursor.execute('DELETE FROM coin')
        con.commit()
        messagebox.showinfo("Clear Portfolio", "Portfolio cleared!")
        ekran_temizle()

    def exit_app():
        window.destroy()

    menu = Menu(window)
    file_item = Menu(menu)
    file_item.add_command(label='Clear Portfolio', command=clear_portfolio)
    file_item.add_command(label='Exit', command=exit_app)
    menu.add_cascade(label='File', menu=file_item)

    help_item = Menu(menu)
    help_item.add_command(label='Clear Portfolio', command=clear_portfolio)
    help_item.add_command(label='Exit', command=exit_app)
    menu.add_cascade(label='Help', menu=help_item)

    window.config(menu=menu)

def my_portfolio():
    api_request = requests.get("https://pro-api.coinmarketcap.com/v1/cryptocurrency"
                               "/listings/latest?start=1&limit=10&convert=USD&"
                               "CMC_PRO_API_KEY=f1e4d2c9-ca98-4890-8b29-70ee91a81a86")

    result = json.loads(api_request.content)

    cursor.execute("SELECT * from coin order by id")
    sepet = cursor.fetchall()

    portfoy_karzarar = 0

    all_amount_paid = 0

    satir_no = 1

    for coin in sepet:
        for i in range(10):
            if result["data"][i]["symbol"] == coin[1]:
                yuvarlak_current = round(result["data"][i]["quote"]["USD"]["price"], 2)
                coin_basina_karzarar = yuvarlak_current - coin[3]
                toplam_maliyet = coin[2] * coin[3]
                toplam_karzarar = coin_basina_karzarar * coin[2]
                portfoy_karzarar = portfoy_karzarar + toplam_karzarar

                portfolio_id = Label(window, text=coin[0], bg='#d1d1cf', fg='black',
                             borderwidth=2, relief='groove', padx=2, pady=2,
                             font='Lato 12')
                portfolio_id.grid(row=satir_no, column=0, sticky=N + S + W + E)

                name = Label(window, text=coin[1], bg='#d1d1cf', fg='black',
                             borderwidth=2, relief='groove', padx=2, pady=2,
                             font='Lato 12')
                name.grid(row=satir_no, column=1, sticky=N+S+W+E)

                price = Label(window, text=turkish_formatla(coin[3]), fg='black',
                              bg='#d1d1cf',
                              borderwidth = 2, relief = 'groove', padx = 2, pady = 2,
                              font='Lato 12')
                price.grid(row=satir_no, column=2, sticky=N+S+W+E)

                no_coins = Label(window, text=coin[2], bg='#d1d1cf', fg='black',
                                 borderwidth=2, relief='groove', padx=2, pady=2,
                                 font='Lato 12')
                no_coins.grid(row=satir_no, column=3, sticky=N+S+W+E)

                amount_paid = Label(window, text=turkish_formatla(toplam_maliyet), fg='black',
                                    bg='#d1d1cf',
                                    borderwidth=2, relief='groove', padx=2, pady=2,
                                    font='Lato 12')
                amount_paid.grid(row=satir_no, column=4, sticky=N+S+W+E)

                all_amount_paid = all_amount_paid + toplam_maliyet



                current_val = Label(window, text=turkish_formatla(yuvarlak_current),
                                    bg='#d1d1cf', fg='black',
                                    borderwidth=2, relief='groove', padx=2, pady=2,
                                    font='Lato 12')
                current_val.grid(row=satir_no, column=5, sticky=N+S+W+E)

                pl_coin = Label(window, text=turkish_formatla(coin_basina_karzarar),
                                fg=font_color_pl(coin_basina_karzarar),
                                bg='#d1d1cf',
                                borderwidth=2, relief='groove', padx=2, pady=2,
                                font='Lato 12')
                pl_coin.grid(row=satir_no, column=6, sticky=N+S+W+E)

                total_pl = Label(window, text=turkish_formatla(toplam_karzarar),
                                 bg='#d1d1cf', fg=font_color_pl(toplam_karzarar),
                                 borderwidth=2, relief='groove', padx=2, pady=2,
                                 font='Lato 12', anchor='e')
                total_pl.grid(row=satir_no, column=7, sticky=E+W)

                satir_no = satir_no + 1

    all_amount_paid_label = Label(window, text=turkish_formatla(all_amount_paid),
                         bg='#d1d1cf', fg='black',
                         borderwidth=2, relief='groove', padx=2, pady=2,
                         font='Lato 12')
    all_amount_paid_label.grid(row=satir_no, column=4, sticky=N + S + W + E)

    portfolio_pl = Label(window, text=turkish_formatla(portfoy_karzarar),
                     bg='#d1d1cf', fg=font_color_pl(portfoy_karzarar),
                     borderwidth=2, relief='groove', padx=2, pady=2,
                     font='Lato 12', anchor='e')
    portfolio_pl.grid(row=satir_no, column=7, sticky=N + S + W + E)

    # Add coin ekliyoruz.
    global portfolio_id_text
    portfolio_id_text = StringVar()
    portfolio_id_entry = Entry(window, borderwidth=2, relief='groove',
                               textvariable=portfolio_id_text, width=5)
    portfolio_id_entry.grid(row=satir_no+1, column=0, sticky=W + E)

    global symbol_text
    symbol_text = StringVar()
    symbol_entry = Entry(window, borderwidth=2, relief='groove',
                               textvariable=symbol_text, width=5)
    symbol_entry.grid(row=satir_no + 1, column=1, sticky=W + E)

    global price_text
    price_text = StringVar()
    price_entry = Entry(window, borderwidth=2, relief='groove',
                               textvariable=price_text, width=5)
    price_entry.grid(row=satir_no + 1, column=2, sticky=W + E)

    global amount_text
    amount_text = StringVar()
    amount_entry = Entry(window, borderwidth=2, relief='groove',
                               textvariable=amount_text, width=5)
    amount_entry.grid(row=satir_no + 1, column=3, sticky=W + E)

    add_button = Button(window, text="Add Coin",
                            bg='blue', fg='white',
                            borderwidth=2, relief='groove', padx=2, pady=2,
                            font='Lato 12 bold', command=insert_coin)
    add_button.grid(row=satir_no + 1, column=4, sticky=W+E)

    update_button = Button(window, text="Update Coin",
                        bg='blue', fg='white',
                        borderwidth=2, relief='groove', padx=2, pady=2,
                        font='Lato 12 bold', command=update_coin)
    update_button.grid(row=satir_no + 1, column=5, sticky=W+E)

    delete_button = Button(window, text="Delete Coin",
                           bg='blue', fg='white',
                           borderwidth=2, relief='groove', padx=2, pady=2,
                           font='Lato 12 bold', command=delete_coin)
    delete_button.grid(row=satir_no + 1, column=6, sticky=W + E)

    refresh_button = Button(window, text="Refresh",
                         bg='green', fg='white',
                         borderwidth=2, relief='groove', padx=2, pady=2,
                         font='Lato 12 bold', command=ekran_temizle)
    refresh_button.grid(row=satir_no+1, column=7, sticky=N + S + W + E)






window = Tk()
window.title('My Coin Portfolio')
window.iconbitmap('favicon.ico')

window.geometry('1100x250')
center_window(1100, 250)



def app_header():
    portfolio_id = Label(window, text='Portfolio Id', bg=rgb_color((0, 0, 128)), fg='white',
                 font='Lato 12 bold', borderwidth=2, relief='groove', padx=5, pady=5)
    portfolio_id.grid(row=0, column=0, sticky=N + S + W + E)

    name = Label(window, text='Coin Name', bg=rgb_color((0, 0, 128)), fg='white',
                 font='Lato 12 bold', borderwidth=2, relief='groove', padx=5, pady=5)
    name.grid(row=0, column=1, sticky=N+S+W+E)

    price = Label(window, text='Price', bg=rgb_color((0, 0, 128)), fg='white',
                  font='Lato 12 bold', borderwidth=2, relief='groove', padx=5, pady=5)
    price.grid(row=0, column=2, sticky=N+S+W+E)

    no_coins = Label(window, text='Coin Owned', bg=rgb_color((0, 0, 128)), fg='white',
                     font='Lato 12 bold', borderwidth=2, relief='groove', padx=5, pady=5)
    no_coins.grid(row=0, column=3, sticky=N+S+W+E)

    amount_paid = Label(window, text='Total Amount Paid', bg=rgb_color((0, 0, 128)), fg='white',
                        font='Lato 12 bold', borderwidth=2, relief='groove', padx=5, pady=5)
    amount_paid.grid(row=0, column=4, sticky=N+S+W+E)

    current_val = Label(window, text='Current Value', bg=rgb_color((0, 0, 128)), fg='white',
                        font='Lato 12 bold', borderwidth=2, relief='groove', padx=5, pady=5)
    current_val.grid(row=0, column=5, sticky=N+S+W+E)

    pl_coin = Label(window, text='P/L Per Coin', bg=rgb_color((0, 0, 128)), fg='white',
                    font='Lato 12 bold', borderwidth=2, relief='groove', padx=5, pady=5)
    pl_coin.grid(row=0, column=6, sticky=N+S+W+E)

    total_pl = Label(window, text='Total P/L with Coin', bg=rgb_color((0, 0, 128)), fg='white',
                     font='Lato 12 bold', borderwidth=2, relief='groove', padx=5, pady=5)
    total_pl.grid(row=0, column=7, sticky=N+S+W+E)

db_doldur()
app_menu()
app_header()
my_portfolio()
window.mainloop()


cursor.close()
con.close()



