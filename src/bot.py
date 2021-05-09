from telegram.ext import Updater, CommandHandler, ConversationHandler, RegexHandler, MessageHandler, Filters
from telegram import ChatAction
from config.auth import token

import database

REGISTER_NAME, REGISTER_LAST_NAME, OPCIONES, TRASLADO, RETIRO, CONSIGNACION, CONFIRMACION_TRASLADO, CONFIRMACION_RETIRO, REGISTRO_MOVIMIENTOS = range(
    9)

def start(update, context):
    typing(update, context)
    chat_id = update.effective_chat.id
    user = database.get_user_by_chat_id(chat_id)

    if user == None:
        context.bot.send_message(
            chat_id=chat_id,
            text="Hola, ¿deseas registrarte?"
        )
        return REGISTER_NAME
        database.insert_user(("Test", "Test", chat_id))
    else:
        context.bot.send_message(
            chat_id=chat_id,
            text="Hola %s, ¿en qué puedo ayudarte?\n "
                 "Recuerda que puedes usar los siguientes comandos:\n"
                 "/subir_trabajo -> Para registrar un nuevo trabajo\n "
                 "/consultar -> Para consultar el estado de un trabajo"
                 "/ayuda -> Para listar todos los comandos disponibles" % user.name
        )

    #si está registrado
    # return


def register_name(update, context):
    user_response = update.message.text
    user = update.message.from_user

    if user_response.lower() == "si":
        update.message.reply_text('Ingresa tu nombre por favor')
        return REGISTER_LAST_NAME
    else:
        update.message.reply_text("Ok %s, ¡que tengas un lindo día!" % user.first_name)

def register_last_name(update, context):
    name = update.message.text

    update.message.reply_text('Ingresa tu apellido por favor')


def incorrect_response(update, context):
    user = update.message.from_user

    msg = "%s Recuerda responder *Si* en caso afirmativo, *No* en caso negativo. ¿Deseas registrarte?" % user.first_name
    update.message.reply_text(msg)

    return REGISTER_NAME

def invalid_name(update, context):
    user = update.message.from_user

    msg = "El nombre ingresado es inválido, ingresalo de nuevo por favor" ## AQUI EL FLUJO NO ESTÁ CUADRANDO MIRAR BIEN
    update.message.reply_text(msg)

    return REGISTER_NAME

def typing(update, context):
    context.bot.sendChatAction(chat_id=update.effective_chat.id,
                               action=ChatAction.TYPING)


if __name__ == '__main__':
    database.create_db()
    updater = Updater(token=token)
    dispatcher = updater.dispatcher

    conversation_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],

        states={
            REGISTER_NAME: [RegexHandler('^(SI|si|Si)$', register_name),
                          MessageHandler(Filters.text, incorrect_response)],

            REGISTER_LAST_NAME: [
                RegexHandler('^([a-z]*[A-Z]*\D)+$', register_last_name),
                MessageHandler(Filters.text, registro_incorrecto_p2)],

            REGISTER_USER: [RegexHandler('^([a-z]*[A-Z]*\D)+$', opciones),
                       MessageHandler(Filters.text, opciones_incorrecto)],

            TRASLADO: [RegexHandler('^\d+\s?\-\s?\d+$', traslados), MessageHandler(Filters.text, traslado_incorrecto)],

            CONFIRMACION_TRASLADO: [RegexHandler('^\d+\s?-\s?(A|a|C|c)$', confirmacion_traslado),
                                    MessageHandler(Filters.text, confirmacionT_incorrecto)],

            RETIRO: [RegexHandler('^\d+$', retiros), MessageHandler(Filters.text, retiro_incorrecto)],

            CONFIRMACION_RETIRO: [RegexHandler('^\d+\s?-\s?(A|a|C|c)$', confirmacion_retiro),
                                  MessageHandler(Filters.text, confirmacionR_incorrecto)],

            CONSIGNACION: [RegexHandler('^\d+$', consignaciones), MessageHandler(Filters.text, consig_incorrecto)],

        },

        fallbacks=[CommandHandler('cancel', cancelar), CommandHandler("micuenta", micuenta),
                   CommandHandler("help", help)]
    )

    dispatcher.add_handler(conversation_handler)

    # dispatcher.add_handler(CommandHandler('start', start))

    updater.start_polling()
    updater.idle()
