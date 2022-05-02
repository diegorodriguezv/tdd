import poplib

prev = 0
while True:
    mail = poplib.POP3_SSL("pop.gmail.com")
    mail.user("diegortest1@gmail.com")
    mail.pass_("ilttsyzksdwjzxnc")
    count, total = mail.stat()
    print(total, "remaining", total - prev)
    prev = total
    for msg_num in range(1, count + 1):
        mail.retr(msg_num)
    mail.quit()
