from mail import mail


def give_responses(text):
    if text in ("hello", "hi"):
        return "Hey!"
    if text in ("ss"):
        return "Screenshot Taken:"
    if text in ("image"):
        return "Send an Image for Recognition"
    if text in "email":
        mail()
        return "Mail sent"

    return "Sorry! I can't answer that now"