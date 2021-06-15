import os

from telegram.ext import Updater, CommandHandler, ConversationHandler, RegexHandler, MessageHandler, Filters
from telegram import ChatAction
from config.auth import token
from user import User
from task import Task

import database

REGISTER, SUCCESSFUL_REGISTER, UPLOAD_TASK, CONSULT_TASK = range(4)


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


def upload_task_option(update, context):
    typing(update, context)
    chat_id = update.effective_chat.id
    user = User.get_user_by_chat_id(chat_id)

    if user is None:
        context.bot.send_message(
            chat_id=chat_id,
            text="Parece que no estás registrado, ¿deseas registrarte?"
        )
        return REGISTER

    else:
        context.bot.send_message(
            chat_id=chat_id,
            text="%s, por favor ingresa la URL del trabajo que deseas subir" % user.name
        )
        return UPLOAD_TASK


def consult_option(update, context):
    typing(update, context)
    chat_id = update.effective_chat.id
    user = User.get_user_by_chat_id(chat_id)

    if user is None:
        context.bot.send_message(
            chat_id=chat_id,
            text="Parece que no estás registrado, ¿deseas registrarte?"
        )
        return REGISTER

    else:
        context.bot.send_message(
            chat_id=chat_id,
            text="%s, por favor ingresa el identificador del trabajo que deseas consultar" % user.name
        )
        return CONSULT_TASK


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

    msg = "¡Tu registro ha sido exitoso %s!\n" \
          "Con los siguientes comandos puedes interactuar conmigo:\n" \
          "/subir_trabajo Para registrar un nuevo trabajo\n" \
          "/consultar Para consultar el estado de un trabajo\n" \
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


def upload_task(update, context):
    task_link = update.message.text
    chat_id = update.effective_chat.id
    user = User.get_user_by_chat_id(chat_id)

    typing(update, context)

    task_already_created = Task.get_task_by_user_and_link(user.id, task_link)

    if task_already_created is None:
        task = Task(task_link, user.id)
        task_id = task.register()

        msg = "Tu trabajo se subió exitosamente, con el siguiente " \
              "identificador podrás consultar su estado --> %s.\n" \
              "Recuerda que puedes usar el comando /consultar" % task_id

        context.bot.send_message(
            chat_id=chat_id,
            text=msg
        )
        return ConversationHandler.END

    else:
        context.bot.send_message(
            chat_id=chat_id,
            text="%s, este trabajo ya lo subiste hace unos días" % user.name
        )
        return ConversationHandler.END


def invalid_task_link(update, context):
    chat_id = update.effective_chat.id

    context.bot.send_message(
        chat_id=chat_id,
        text="El link que ingresaste es inválido, ¡intenta de nuevo!"
    )

    return UPLOAD_TASK


def consult_task(update, context):
    task_id = update.message.text
    chat_id = update.effective_chat.id
    user = User.get_user_by_chat_id(chat_id)

    task = Task.get_task_by_id_and_user(task_id, user.id)

    if task is None:
        context.bot.send_message(
            chat_id=chat_id,
            text="%s, no tienes ningún trabajo con el identificador ingresado" % user.name
        )
        return ConversationHandler.END
    else:
        msg = ""
        if task.state == "on hold":
            msg = "Este trabajo se encuentra **en espera** de ser revisado"

        elif task.state == "graded":
            msg = "Este trabajo ya fue **calificado**, tiene una calificación de %s" % str(task.grade)

        context.bot.send_message(
            chat_id=chat_id,
            text=msg
        )
        return ConversationHandler.END

def invalid_task_id(update, context):
    chat_id = update.effective_chat.id

    context.bot.send_message(
        chat_id=chat_id,
        text="El identificador que ingresaste es inválido, ¡intenta de nuevo!"
    )

    return CONSULT_TASK


def typing(update, context):
    context.bot.sendChatAction(chat_id=update.effective_chat.id,
                               action=ChatAction.TYPING)


if __name__ == '__main__':
    if not os.path.exists('bot.db'):
        database.create_db()

    updater = Updater(token=token)
    dispatcher = updater.dispatcher

    conversation_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start), CommandHandler('subir_trabajo', upload_task_option),
                      CommandHandler('consultar', consult_option)],

        states={
            REGISTER: [MessageHandler(Filters.regex('^(SI|si|Si|NO|no|No)$'), register),
                       MessageHandler(Filters.text, incorrect_response)],

            SUCCESSFUL_REGISTER: [
                MessageHandler(Filters.regex('^([a-z]*[A-Z]*\D)+\s([a-z]*[A-Z]*\D)+$'), successful_register),
                MessageHandler(Filters.text, invalid_register)],

            UPLOAD_TASK: [
                MessageHandler(Filters.regex('^(http(s)?:\/\/.+)$'), upload_task),
                MessageHandler(Filters.text, invalid_task_link)],

            CONSULT_TASK: [
                MessageHandler(Filters.regex('^(\d+)$'), consult_task),
                MessageHandler(Filters.text, invalid_task_id)],

        },
        fallbacks=[]

        # fallbacks=[CommandHandler('cancel', cancelar), CommandHandler("micuenta", micuenta),
        #            CommandHandler("help", help)]
    )

    dispatcher.add_handler(conversation_handler)

    # dispatcher.add_handler(CommandHandler('start', start))

    updater.start_polling()
    updater.idle()
