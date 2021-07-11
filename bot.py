import os

from telegram.ext import Updater, CommandHandler, ConversationHandler, MessageHandler, Filters
from src.config.auth import token

import src.DB.database as database
import src.modules.commands_handlers as commands_handlers

REGISTER, SUCCESSFUL_REGISTER, UPLOAD_TASK, CONSULT_TASK, EDIT_TASK, DELETE_TASK = range(6)

if __name__ == '__main__':
    if not os.path.exists('src/DB/bot.db'):
        database.create_db()

    updater = Updater(token=token)
    dispatcher = updater.dispatcher

    conversation_handler = ConversationHandler(
        entry_points=[CommandHandler('start', commands_handlers.start), CommandHandler('subir', commands_handlers.upload_task_option),
                      CommandHandler('consultar', commands_handlers.consult_option), CommandHandler('listar', commands_handlers.list_tasks_option,),
                      CommandHandler('editar', commands_handlers.edit_option), CommandHandler('eliminar', commands_handlers.delete_option),
                      CommandHandler('ayuda', commands_handlers.help_option)],

        states={
            REGISTER: [MessageHandler(Filters.regex('^(SI|si|Si|NO|no|No)$'), commands_handlers.register),
                       MessageHandler(Filters.text, commands_handlers.incorrect_response)],

            SUCCESSFUL_REGISTER: [
                MessageHandler(Filters.regex('^([a-z]*[A-Z]*\D)+\s([a-z]*[A-Z]*\D)+$'), commands_handlers.successful_register),
                MessageHandler(Filters.text, commands_handlers.invalid_register)],

            UPLOAD_TASK: [
                MessageHandler(Filters.regex('^(http(s)?:\/\/[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}([-a-zA-Z0-9()@:%_\+.~#?&//=]*))$'), commands_handlers.upload_task),
                MessageHandler(Filters.text, commands_handlers.invalid_task_link)],

            CONSULT_TASK: [
                MessageHandler(Filters.regex('^(\d+)$'), commands_handlers.consult_task),
                MessageHandler(Filters.text, commands_handlers.invalid_task_id)],

            EDIT_TASK: [
                MessageHandler(Filters.regex('^(\d+\s+http(s)?:\/\/[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}([-a-zA-Z0-9()@:%_\+.~#?&//=]*))$'), commands_handlers.edit_task),
                MessageHandler(Filters.text, commands_handlers.invalid_edition_info)],

            DELETE_TASK: [
                MessageHandler(Filters.regex('^(\d+)$'), commands_handlers.delete_task),
                MessageHandler(Filters.text, commands_handlers.invalid_task_id_deletion)],

        },
        fallbacks=[]
    )

    dispatcher.add_handler(conversation_handler)

    # updater.start_polling()

    # For heroku
    PORT = int(os.environ.get('PORT', '8443'))
    updater.start_webhook(listen="0.0.0.0",
                          port=PORT,
                          url_path=token,
                          webhook_url="https://afternoon-retreat-75061.herokuapp.com/" + token)

    updater.idle()
