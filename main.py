import pymysql
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram import ChatAction


def start(bot, update):
    bot.sendChatAction(update.message.chat_id, ChatAction.TYPING)
    nome = update.message.from_user.first_name
    dft = "Welcome on this bot, "
    update.message.reply_text(dft + nome)


def show(bot, update):
    global conn
    select_all = "select todo\nfrom task\norder by todo;"

    bot.sendChatAction(update.message.chat_id, ChatAction.TYPING)
    cursor = conn.cursor()
    cursor.execute(select_all)
    ris = cursor.fetchall()
    cursor.close()
    if len(ris) > 0:
        update.message.reply_text(ris)
    else:
        update.message.reply_text("Nothing to do here!")


def new(bot, update, args):
    global conn
    insert = "insert into task(todo) values(%s);"

    bot.sendChatAction(update.message.chat_id, ChatAction.TYPING)
    cursor = conn.cursor()
    nuovo = " ".join(args)
    cursor.execute(insert, (nuovo, ))
    conn.commit()
    update.message.reply_text("The new task was succesfully added to the list!")
    cursor.close()


def rm(bot, update, args):
    global conn
    delete_one = "delete from task where todo=%s;"

    bot.sendChatAction(update.message.chat_id, ChatAction.TYPING)
    cursor = conn.cursor()
    togli = " ".join(args)
    rows = cursor.execute(delete_one, (togli,))
    if rows > 0:
        conn.commit()
        update.message.reply_text("The task was successfully deleted!\n")
    else:
        update.message.reply_text("The task you specified is not in the list!\n")
    cursor.close()


def rall(bot, update, args):
    global conn
    select_like = "select todo\n from task\n where todo like %s;"
    delete_like = "delete from task\nwhere todo like %s;"

    bot.sendChatAction(update.message.chat_id, ChatAction.TYPING)
    togli = " ".join(args)
    cursor = conn.cursor()
    rows = cursor.execute(select_like, ("%"+togli+"%",))
    if rows == 0:
        update.message.reply_text("I did not find any task to delete!")
    else:
        ris = cursor.fetchall()
        for x in ris:
            stringato = str(x)
            update.message.reply_text("Task '"+stringato[2:-3]+"' removed successfully\n")
        cursor.execute(delete_like, ("%" + togli + "%",))
        conn.commit()
    cursor.close()


def error(bot, update):
    bot.sendChatAction(update.message.chat_id, ChatAction.TYPING)
    update.message.reply_text("I'm sorry, i can only accept one of the 4 commands")


def main():
    upd = Updater(token='hello')

    dp = upd.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("show_tasks", show))
    dp.add_handler(CommandHandler("new_task", new, pass_args=True))
    dp.add_handler(CommandHandler("remove_task", rm, pass_args=True))
    dp.add_handler(CommandHandler("remove_all_tasks", rall, pass_args=True))
    dp.add_handler(MessageHandler(Filters.text, error))

    upd.start_polling()
    upd.idle()


if __name__ == '__main__':
    conn = pymysql.connect(user="utente", password="piru",
                            host="localhost", database="tasklist")
    main()
    conn.close()
    print("done here")


