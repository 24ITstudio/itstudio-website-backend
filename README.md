
# itstudio website backend

Backend for itstudio website

## Conf

### Enroll DDL

search in order:

- DDL variable in website/enroll/_ddl_conf.py
- DDL env variable

### Email sending server 
For security reasons,
when it comes to email user and password,
we do not rely on configure in `website/website/settings.py`,

but use a lazy-load mechanism:

If no valid configure about email auth is given,
the server will only raise OSError when `enroll.verify_code.send_code` is called.

And where to put configure about email auth, like user and password?

The answer is `website/enroll/_email_conf.py`, which is already put in `.gitignore`

For example, assuming your email user and password is `User` and `Pwd`,
then you can type the following to `website/enroll/_email_conf.py`:

```Python
EMAIL_HOST_USER = r"User"
EMAIL_HOST_PASSWORD = r"Pwd"
```

And you won't need to worry about these infomation being leak,
as this file will be ignored by `git` and you can freely execuate command like `git add .`.

If you wanna use configure defined at 
`website/website/settings.py`,
just delete `website/enroll/_email_conf.py` and here you go.
