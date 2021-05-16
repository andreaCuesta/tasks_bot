import os

from telegram.ext import Updater, CommandHandler, ConversationHandler, RegexHandler, MessageHandler, Filters
from telegram import ChatAction
from config.auth import token
from user import User

import database

REGISTER, SUCCESSFUL_REGISTER = range(2)

def start(update, context):
    typing(update, context)
    chat_id = update.effective_chat.id
    user = User.get_user_by_chat_id(chat_id)

    if user is None:
        context.bot.send_message(
            chat_id=chat_id,
            text="Hola, ¿deseas registrarte?"
        )
        return REGISTER

    else:
        context.bot.send_message(
            chat_id=chat_id,
            text="Hola %s, ¿en qué puedo ayudarte?\n"
                 "Recuerda que puedes usar los siguientes comandos:\n"
                 "/subir_trabajo Para registrar un nuevo trabajo\n"
                 "/consultar Para consultar el estado de un trabajo\n"
                 "/ayuda Para listar todos los comandos disponibles" % user.name
        )
        return ConversationHandler.END


def register(update, context):
    user_response = update.message.text
    user = update.message.from_user

    if user_response.lower() == "si":
        update.message.reply_text('Ingresa tu nombre completo por favor')
        return SUCCESSFUL_REGISTER
    else:
        update.message.reply_text("Ok %s, ¡que tengas un lindo día!" % user.first_name)
        return ConversationHandler.END

def successful_register(update, context):
    full_name = update.message.text.split()
    chat_id = update.effective_chat.id

    user = User(full_name[0], full_name[1], chat_id)
    user.register()

    msg = "¡Tu registro ha sido exitoso %s!\n"\
          "Con los siguientes comandos puedes interactuar conmigo:\n"\
          "/subir_trabajo Para registrar un nuevo trabajo\n"\
          "/consultar Para consultar el estado de un trabajo\n"\
          "/ayuda Para listar todos los comandos disponibles" % user.name

    update.message.reply_text(msg)
    return ConversationHandler.END

def incorrect_response(update, context):
    user = update.message.from_user

    msg = "%s Recuerda responder *Si* en caso afirmativo, *No* en caso negativo. ¿Deseas registrarte?" % user.first_name
    update.message.reply_text(msg)

    return REGISTER

def invalid_register(update, context):
    user = update.message.from_user

    msg = "El nombre ingresado es inválido, ¿deseas ingresarlo de nuevo?"
    update.message.reply_text(msg)

    return REGISTER

def typing(update, context):
    context.bot.sendChatAction(chat_id=update.effective_chat.id,
                               action=ChatAction.TYPING)


if __name__ == '__main__':
    if not os.path.exists('bot.db'):
        database.create_db()

    updater = Updater(token=token)
    dispatcher = updater.dispatcher

    conversation_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],

        states={
            REGISTER: [MessageHandler(Filters.regex('^(SI|si|Si|NO|no|No)$'), register),
                          MessageHandler(Filters.text, incorrect_response)],

            SUCCESSFUL_REGISTER: [
                MessageHandler(Filters.regex('^([a-z]*[A-Z]*\D)+\s([a-z]*[A-Z]*\D)+$'), successful_register),
                MessageHandler(Filters.text, invalid_register)],

        },
        fallbacks=[]

        # fallbacks=[CommandHandler('cancel', cancelar), CommandHandler("micuenta", micuenta),
        #            CommandHandler("help", help)]
    )

    dispatcher.add_handler(conversation_handler)

    # dispatcher.add_handler(CommandHandler('start', start))

    updater.start_polling()
    updater.idle()
