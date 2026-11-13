import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from flask import Flask
import threading
import os

TOKEN = os.environ.get('BOT_TOKEN', '9239108617:AAGhykdVwOEvpyRzG6zuF9mFhhvhxnp8sAY')
bot = telebot.TeleBot(TOKEN)

app = Flask(__name__)

@app.route('/')
def index():
    return "Spor Arena Bot çalışıyor!"

@app.route('/health')
def health():
    return "OK", 200

def run_flask():
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)

def ana_menu_olustur():
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("📰 Son Dakika Haberleri", callback_data="haberler"))
    markup.add(InlineKeyboardButton("🔄 Transfer Gelişmeleri", callback_data="transferler"))
    markup.add(InlineKeyboardButton("⚽️ Futbol Puan Durumları", callback_data="futbol_puan"))
    markup.add(InlineKeyboardButton("🏀 Basketbol Puan Durumu", callback_data="basket_puan"))
    return markup

@bot.message_handler(commands=['start'])
def send_welcome(message):
    metin = (
        f"Merhaba {message.from_user.first_name}! ⚽️🏀\n\n"
        "**Spor Arena'ya hoş geldin!**\n"
        "Türkiye ve dünya sporundan son dakika haberleri, transfer gelişmeleri, "
        "majör liglerin puan durumları ve basketbol verileri burada.\n\n"
        "Aşağıdaki menüden bir kategori seç:"
    )
    bot.send_message(message.chat.id, metin, reply_markup=ana_menu_olustur(), parse_mode='Markdown')

@bot.message_handler(commands=['yardim'])
def send_help(message):
    bot.send_message(message.chat.id, "Menüdeki butonları kullanarak haberlere, transferlere ve puan durumlarına ulaşabilirsin. /start ile ana menüye dönebilirsin.")

@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    if call.data == "geri_don":
        bot.edit_message_text(
            chat_id=call.message.chat.id, message_id=call.message.message_id,
            text="**Spor Arena Ana Menü**\n\nKategori seç:",
            reply_markup=ana_menu_olustur(), parse_mode='Markdown'
        )
        return

    geri = InlineKeyboardMarkup()
    geri.add(InlineKeyboardButton("🔙 Ana Menü", callback_data="geri_don"))

    if call.data == "haberler":
        metin = (
            "📰 **Son Dakika Spor Haberleri**\n\n"
            "🔹 **Futbol:** Süper Lig'de derbi haftası yaklaşıyor. Galatasaray, Fenerbahçe, Beşiktaş ve Trabzonspor'un son antrenman raporları açıklandı. Sakatlık durumları kritik önem taşıyor.\n\n"
            "🔹 **Transfer:** Cristiano Ronaldo'nun menajeri aracılığıyla Süper Lig'in 4 büyük kulübüne önerildiği iddia edildi. 41 yaşındaki yıldızın Suudi Arabistan sözleşmesi 2027'de bitiyor [citation:1].\n\n"
            "🔹 **Basketbol:** EuroLeague'de temsilcilerimiz bu hafta kritik maçlara çıkıyor. Fenerbahçe ve Anadolu Efes, play-off yarışında hayati önem taşıyan karşılaşmalar oynayacak."
        )
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=metin, reply_markup=geri, parse_mode='Markdown')

    elif call.data == "transferler":
        metin = (
            "🔄 **Transfer Piyasası**\n\n"
            "📌 **Süper Lig:** Sezon başında büyük transferler yapıldı. Trabzonspor, Mohamed Salah ile 2 yıllık sözleşme imzaladı. Beşiktaş, Dusan Vlahovic'i kadrosuna kattı. Galatasaray, Rafael Leao'yu transfer etti. Fenerbahçe, Romelu Lukaku ile anlaştı [citation:8].\n\n"
            "📌 **Fenerbahçe Gündemi:** Teknik direktör Emre Belözoğlu, Ocak ayında mutlak bir golcü istiyor. Inter'le sözleşme görüşmeleri tıkanan Marcus Thuram'ın menajeri Fenerbahçe'nin kapısına geldi [citation:15].\n\n"
            "📌 **Beşiktaş:** Brahim Diaz transferi için Real Madrid ile görüşmeler sürüyor. Başkan Serdal Adalı, oyuncunun babasıyla İstanbul'da görüştü [citation:15]."
        )
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=metin, reply_markup=geri, parse_mode='Markdown')

    elif call.data == "futbol_puan":
        alt_menu = InlineKeyboardMarkup()
        alt_menu.add(InlineKeyboardButton("🇹🇷 Süper Lig", callback_data="puan_super"))
        alt_menu.add(InlineKeyboardButton("🏴󠁧󠁢󠁥󠁮󠁧󠁿 Premier Lig", callback_data="puan_premier"))
        alt_menu.add(InlineKeyboardButton("🇪🇸 La Liga", callback_data="puan_laliga"))
        alt_menu.add(InlineKeyboardButton("🔙 Ana Menü", callback_data="geri_don"))
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="⚽️ **Hangi ligin puan durumunu görmek istersin?**", reply_markup=alt_menu, parse_mode='Markdown')

    elif call.data == "puan_super":
        metin = (
            "🇹🇷 **Süper Lig Puan Durumu (2026-27 Sezonu)**\n\n"
            "1. Galatasaray - 28 Puan (11 Maç)\n"
            "2. Trabzonspor - 25 Puan (11 Maç)\n"
            "3. Göztepe - 23 Puan (11 Maç)\n"
            "4. Beşiktaş - 22 Puan (11 Maç)\n"
            "5. Kasımpaşa - 20 Puan (11 Maç)\n"
            "6. Fenerbahçe - 19 Puan (11 Maç)\n"
            "7. Kocaelispor - 19 Puan (11 Maç)\n"
            "8. Başakşehir - 17 Puan (11 Maç)\n\n"
            "*Kaynak: Güncel lig verileri [citation:9]*"
        )
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=metin, reply_markup=geri, parse_mode='Markdown')

    elif call.data == "puan_premier":
        metin = (
            "🏴󠁧󠁢󠁥󠁮󠁧󠁿 **Premier Lig Puan Durumu (2025-26 Sezonu)**\n\n"
            "1. Arsenal - 85 Puan (38 Maç)\n"
            "2. Manchester City - 78 Puan (38 Maç)\n"
            "3. Manchester United - 71 Puan (38 Maç)\n"
            "4. Aston Villa - 65 Puan (38 Maç)\n"
            "5. Liverpool - 60 Puan (38 Maç)\n\n"
            "*Kaynak: Premier League resmi verileri [citation:3]*"
        )
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=metin, reply_markup=geri, parse_mode='Markdown')

    elif call.data == "puan_laliga":
        metin = (
            "🇪🇸 **La Liga Puan Durumu (2026-27 Sezonu)**\n\n"
            "1. Barcelona - 33 Puan (12 Maç)\n"
            "2. Real Madrid - 30 Puan (12 Maç)\n"
            "3. Atletico Madrid - 28 Puan (12 Maç)\n"
            "4. Real Betis - 26 Puan (12 Maç)\n"
            "5. Real Sociedad - 22 Puan (12 Maç)\n\n"
            "*Kaynak: La Liga güncel verileri [citation:4][citation:11]*"
        )
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=metin, reply_markup=geri, parse_mode='Markdown')

    elif call.data == "basket_puan":
        metin = (
            "🏀 **EuroLeague Puan Durumu (2026 Sezonu)**\n\n"
            "1. Panathinaikos - 8 Galibiyet / 2 Mağlubiyet\n"
            "2. Valencia - 8 Galibiyet / 3 Mağlubiyet\n"
            "3. Olympiacos - 8 Galibiyet / 3 Mağlubiyet\n"
            "4. Barcelona - 7 Galibiyet / 3 Mağlubiyet\n"
            "5. Real Madrid - 7 Galibiyet / 4 Mağlubiyet\n"
            "6. Kızıl Yıldız - 7 Galibiyet / 4 Mağlubiyet\n"
            "7. Fenerbahçe - 7 Galibiyet / 4 Mağlubiyet\n"
            "8. Žalgiris - 7 Galibiyet / 4 Mağlubiyet\n\n"
            "*Kaynak: EuroLeague güncel verileri [citation:5][citation:12]*"
        )
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=metin, reply_markup=geri, parse_mode='Markdown')

@bot.message_handler(func=lambda message: True)
def echo_all(message):
    bot.reply_to(message, "Spor Arena botuna hoş geldiniz! Menüyü görmek için /start komutunu kullanın.")

if __name__ == '__main__':
    threading.Thread(target=run_flask, daemon=True).start()
    print("Bot çalışıyor...")
    bot.infinity_polling()
