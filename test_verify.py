from models import verify_password, create_user, get_user_by_email

user = get_user_by_email('test@example.com')
if not user:
    user = create_user('test@example.com','Test','1234567890','password')
    print('created user', user)
else:
    print('existing user', user)

print('verify correct:', verify_password('test@example.com','password'))
print('verify wrong:', verify_password('test@example.com','wrong'))
