import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from flask import Flask
import threading
import os

# Token'ı ortam değişkeninden oku (Render'da ayarlayacağız)
TOKEN = os.environ.get('BOT_TOKEN', '9239108617:AAGhykdVwOEvpyRzG6zuF9mFhhvhxnp8sAY')
bot = telebot.TeleBot(TOKEN)

# --- Flask sunucusu (Render'ın port gereksinimini karşılamak için) ---
app = Flask(__name__)

@app.route('/')
def index():
    return "Spor Arena Bot çalışıyor!"

@app.route('/health')
def health():
    return "OK", 200

def run_flask():
    # Render, PORT ortam değişkenini otomatik olarak atar
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)

# --- Bot menü fonksiyonu (orijinalinden değişmedi) ---
def ana_menu_olustur():
    markup = InlineKeyboardMarkup()
    btn_haberler = InlineKeyboardButton("📰 Son Dakika Haberleri", callback_data="haberler")
    btn_transferler = InlineKeyboardButton("🔄 Transfer Gelişmeleri", callback_data="transferler")
    btn_skorlar = InlineKeyboardButton("⚽️ Günün Skorları", callback_data="skorlar")
    btn_puan = InlineKeyboardButton("📊 Puan Durumu", callback_data="puan")
    markup.add(btn_haberler)
    markup.add(btn_transferler)
    markup.add(btn_skorlar)
    markup.add(btn_puan)
    return markup

@bot.message_handler(commands=['start'])
def send_welcome(message):
    karsilama_metni = (
        f"Merhaba {message.from_user.first_name}! ⚽️\n\n"
        "**Spor Arena'ya hoş geldin!**\n"
        "Güncel spor haberleri, transfer gelişmeleri ve maç skorları için "
        "aşağıdaki menüyü kullanabilirsin."
    )
    bot.send_message(message.chat.id, karsilama_metni, reply_markup=ana_menu_olustur(), parse_mode='Markdown')

@bot.message_handler(commands=['yardim'])
def send_help(message):
    yardim_metni = (
        "🤖 **Spor Arena Bot Kullanımı**\n\n"
        "Bu bot, spor haberlerini takip etmenizi kolaylaştırmak için tasarlanmıştır.\n"
        "Menüdeki butonları kullanarak haberlere ve skorlara ulaşabilirsiniz.\n\n"
        "Komutlar:\n"
        "/start - Ana menüyü açar\n"
        "/yardim - Bu mesajı gösterir"
    )
    bot.send_message(message.chat.id, yardim_metni, parse_mode='Markdown')

@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    if call.data == "geri_don":
        bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text="Spor Arena'ya hoş geldin! ⚽️\nGüncel spor haberleri ve skorlar için menüyü kullanabilirsin.",
            reply_markup=ana_menu_olustur()
        )
        return

    geri_butonu = InlineKeyboardMarkup()
    geri_butonu.add(InlineKeyboardButton("🔙 Ana Menü", callback_data="geri_don"))

    if call.data == "haberler":
        metin = "📰 **Son Dakika Haberleri:**\n\n1. Fenerbahçe'de flaş ayrılık iddiası!\n2. Galatasaray yeni transferini duyurdu.\n3. Beşiktaş derbisi öncesi sakatlık raporu açıklandı."
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=metin, reply_markup=geri_butonu, parse_mode='Markdown')
    elif call.data == "transferler":
        metin = "🔄 **Transfer Gelişmeleri:**\n\n• Oyuncu A, Takım B ile 3 yıllık sözleşme imzaladı.\n• Oyuncu C için Avrupa'dan teklif var.\n• Süper Lig'den bir kulüp, Premier Lig'den golcü arıyor."
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=metin, reply_markup=geri_butonu, parse_mode='Markdown')
    elif call.data == "skorlar":
        metin = "⚽️ **Günün Skorları:**\n\nTakım X 2 - 1 Takım Y\nTakım Z 0 - 0 Takım W\nTakım M 3 - 2 Takım N"
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=metin, reply_markup=geri_butonu, parse_mode='Markdown')
    elif call.data == "puan":
        metin = "📊 **Süper Lig Puan Durumu (İlk 3):**\n\n1. Takım A - 25 Puan\n2. Takım B - 22 Puan\n3. Takım C - 20 Puan"
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=metin, reply_markup=geri_butonu, parse_mode='Markdown')

# --- Flask'ı ayrı bir thread'de başlat, bot polling'i ana thread'de çalıştır ---
if __name__ == '__main__':
    threading.Thread(target=run_flask, daemon=True).start()
    print("Bot çalışıyor...")
    bot.infinity_polling()
