import os

from telegram.ext import Updater, CommandHandler, ConversationHandler, RegexHandler, MessageHandler, Filters
from telegram import ChatAction
from config.auth import token
from user import User
from task import Task

import database

REGISTER, SUCCESSFUL_REGISTER, UPLOAD_TASK, CONSULT_TASK, EDIT_TASK, DELETE_TASK = range(6)


def start(update, context):
    typing(update, context)
    chat_id = update.effective_chat.id
    user = User.get_user_by_chat_id(chat_id)

    msg = ""
    move_to = None

    if user is None:
        msg = "Hola, ¿deseas registrarte?"
        move_to = REGISTER

    else:
        msg = "Hola %s, ¿en qué puedo ayudarte?\n"\
              "Recuerda que puedes usar los siguientes comandos:\n"\
              "/subir_trabajo Para registrar un nuevo trabajo\n"\
              "/consultar Para consultar el estado de un trabajo\n"\
              "/editar Para editar un trabajo existente\n"\
              "/eliminar Para eliminar un trabajo existente\n"\
              "/listar_mis_trabajos Para listar todos los trabajos que has registrado\n"\
              "/ayuda Para listar todos los comandos disponibles" % user.name

        move_to = ConversationHandler.END

    context.bot.send_message(
        chat_id=chat_id,
        text=msg
    )

    return move_to

def upload_task_option(update, context):
    typing(update, context)
    chat_id = update.effective_chat.id
    user = User.get_user_by_chat_id(chat_id)

    msg = ""
    move_to = None

    if user is None:
        msg = "Parece que no estás registrado, ¿deseas registrarte?"
        move_to = REGISTER

    else:
        msg = "%s, por favor ingresa la URL del trabajo que deseas subir" % user.name
        move_to = UPLOAD_TASK

    context.bot.send_message(
        chat_id=chat_id,
        text=msg
    )

    return move_to

def consult_option(update, context):
    typing(update, context)
    chat_id = update.effective_chat.id
    user = User.get_user_by_chat_id(chat_id)

    msg = ""
    move_to = None

    if user is None:
        msg ="Parece que no estás registrado, ¿deseas registrarte?"
        move_to = REGISTER

    else:
        msg = "%s, por favor ingresa el identificador del trabajo que deseas consultar" % user.name
        move_to = CONSULT_TASK

    context.bot.send_message(
        chat_id=chat_id,
        text=msg
    )

    return move_to

def list_tasks_option(update, context):
    typing(update, context)
    chat_id = update.effective_chat.id
    user = User.get_user_by_chat_id(chat_id)

    msg = ""
    move_to = None

    if user is None:
        msg = "Parece que no estás registrado, ¿deseas registrarte?"
        move_to = REGISTER

    else:
        tasks = Task.list_tasks_by_user(user.id)

        if not tasks:
            msg = "%s, no tienes trabajos registrados" % user.name
        else:
            tasks_info = ""

            for task in tasks:
                tasks_info += "* %s , %s , %s , %s \n" %(task.id, task.link, task.status, str(task.grade))

            msg = "%s, a continuación se listan los trabajos que tienes registrados:\n" \
                  "ID , LINK , ESTADO , NOTA \n" % user.name + tasks_info

        move_to = ConversationHandler.END

    context.bot.send_message(
        chat_id=chat_id,
        text=msg
    )

    return move_to

def edit_option(update, context):
    typing(update, context)
    chat_id = update.effective_chat.id
    user = User.get_user_by_chat_id(chat_id)

    msg = ""
    move_to = None

    if user is None:
        msg = "Parece que no estás registrado, ¿deseas registrarte?"
        move_to = REGISTER

    else:
        msg = "%s, por favor ingresa el identificador del trabajo que deseas editar seguido de la nueva url donde lo tienes alojado.\n"\
              "Ejemplo: 12 https://docs.google.com/document/d" % user.name
        move_to = EDIT_TASK

    context.bot.send_message(
        chat_id=chat_id,
        text=msg
    )

    return move_to

def delete_option(update, context):
    typing(update, context)
    chat_id = update.effective_chat.id
    user = User.get_user_by_chat_id(chat_id)

    msg = ""
    move_to = None

    if user is None:
        msg = "Parece que no estás registrado, ¿deseas registrarte?"
        move_to = REGISTER

    else:
        msg = "%s, por favor ingresa el identificador del trabajo que deseas eliminar" % user.name
        move_to = DELETE_TASK

    context.bot.send_message(
        chat_id=chat_id,
        text=msg
    )

    return move_to

def help_option(update, context):
    typing(update, context)
    chat_id = update.effective_chat.id
    user = User.get_user_by_chat_id(chat_id)

    msg = ""
    move_to = None

    if user is None:
        msg = "Parece que no estás registrado, ¿deseas registrarte?"
        move_to = REGISTER

    else:
        msg = "%s, estos son los comandos con los que puedes interactuar conmigo:\n"\
              "/subir_trabajo Para registrar un nuevo trabajo\n"\
              "/consultar Para consultar el estado de un trabajo\n" \
              "/editar Para editar un trabajo existente\n" \
              "/eliminar Para eliminar un trabajo existente\n"\
              "/listar_mis_trabajos Para listar todos los trabajos que has registrado\n"\
              "/ayuda Para listar todos los comandos disponibles" % user.name
        move_to = ConversationHandler.END

    context.bot.send_message(
        chat_id=chat_id,
        text=msg
    )

    return move_to


def register(update, context):
    user_response = update.message.text
    user = update.message.from_user

    msg = ""
    move_to = None

    if user_response.lower() == "si":
        msg = 'Ingresa tu nombre completo por favor'
        move_to = SUCCESSFUL_REGISTER
    else:
        msg = "Ok %s, ¡que tengas un lindo día!" % user.first_name
        move_to = ConversationHandler.END

    update.message.reply_text(msg)
    return move_to

def successful_register(update, context):
    full_name = update.message.text.split()
    chat_id = update.effective_chat.id

    user = User(full_name[0], full_name[1], chat_id)
    user.register()

    msg = "¡Tu registro ha sido exitoso %s!\n" \
          "Con los siguientes comandos puedes interactuar conmigo:\n" \
          "/subir_trabajo Para registrar un nuevo trabajo\n" \
          "/consultar Para consultar el estado de un trabajo\n" \
          "/editar Para editar un trabajo existente\n" \
          "/eliminar Para eliminar un trabajo existente\n" \
          "/listar_mis_trabajos Para listar todos los trabajos que has registrado\n" \
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
    msg = ""

    if task_already_created is None:
        task = Task(task_link, user.id)
        task_id = task.register()

        msg = "Tu trabajo se subió exitosamente, con el siguiente " \
              "identificador podrás consultar su estado --> %s.\n" \
              "Recuerda que puedes usar el comando /consultar" % task_id

    else:
        msg = "%s, este trabajo ya lo subiste hace unos días" % user.name

    context.bot.send_message(
        chat_id=chat_id,
        text=msg
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
    msg = ""

    if task is None:
        msg = "%s, no tienes ningún trabajo con el identificador ingresado" % user.name
    else:
        if task.status == "pendiente":
            msg = "Este trabajo se encuentra **en espera** de ser revisado"

        elif task.status == "calificado":
            msg = "Este trabajo ya fue calificado, tiene una calificación de %s" % str(task.grade)

    context.bot.send_message(
        chat_id=chat_id,
        text=msg
    )

    return ConversationHandler.END

def edit_task(update, context):
    edition_info = update.message.text.split()
    task_id = edition_info[0]
    new_link = edition_info[1]
    chat_id = update.effective_chat.id
    user = User.get_user_by_chat_id(chat_id)

    task = Task.get_task_by_id_and_user(task_id, user.id)
    msg = ""

    if task is None:
        msg = "No tienes ningún trabajo con el identificador ingresado"

    elif task.status == "calificado":
        msg = "Este trabajo ya fue calificado, por tanto, ya no puedes editarlo"

    else:
        updated_task = task.edit(new_link)

        msg = "El trabajo fue editado exitosamente:\n" \
              "ID , LINK , ESTADO \n"\
              "%s , %s , %s" % (updated_task.id, updated_task.link, updated_task.status)

    context.bot.send_message(
        chat_id=chat_id,
        text=msg
    )
    return ConversationHandler.END

def delete_task(update, context):
    task_id = update.message.text
    chat_id = update.effective_chat.id
    user = User.get_user_by_chat_id(chat_id)

    task = Task.get_task_by_id_and_user(task_id, user.id)
    msg = ""

    if task is None:
        msg = "No tienes ningún trabajo con el identificador ingresado"

    elif task.status == "calificado":
        msg = "Este trabajo ya fue calificado, por tanto, ya no puedes eliminarlo"

    else:
        task.delete()
        msg = "El trabajo fue eliminado exitosamente."

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

def invalid_edition_info(update, context):
    chat_id = update.effective_chat.id

    context.bot.send_message(
        chat_id=chat_id,
        text="La información ingresada es inválida, recuerda que debes ingresar el identificador del trabajo que deseas "
             "editar seguido de la nueva url donde lo tienes alojado.\n"
             "Ejemplo: 12 https://docs.google.com/document/d"
    )

    return EDIT_TASK

def invalid_task_id_deletion(update, context):
    chat_id = update.effective_chat.id

    context.bot.send_message(
        chat_id=chat_id,
        text="El identificador que ingresaste es inválido, ¡intenta de nuevo!"
    )

    return DELETE_TASK

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
                      CommandHandler('consultar', consult_option), CommandHandler('listar_mis_trabajos', list_tasks_option,),
                      CommandHandler('editar', edit_option), CommandHandler('eliminar', delete_option),
                      CommandHandler('ayuda', help_option)],

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

            EDIT_TASK: [
                MessageHandler(Filters.regex('^(\d+\s+http(s)?:\/\/(\S.)+)$'), edit_task),
                MessageHandler(Filters.text, invalid_edition_info)],

            DELETE_TASK: [
                MessageHandler(Filters.regex('^(\d+)$'), delete_task),
                MessageHandler(Filters.text, invalid_task_id_deletion)],

        },
        fallbacks=[]

        # fallbacks=[CommandHandler('cancel', cancelar), CommandHandler("micuenta", micuenta),
        #            CommandHandler("help", help)]
    )

    dispatcher.add_handler(conversation_handler)

    # dispatcher.add_handler(CommandHandler('start', start))

    updater.start_polling()
    updater.idle()
