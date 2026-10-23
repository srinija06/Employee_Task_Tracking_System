from utils.validators import is_valid_email

print(is_valid_email("user@gmail.com"))
print(is_valid_email("test.employee@company.com"))
print(is_valid_email("test@"))
print(is_valid_email("invalid-email"))