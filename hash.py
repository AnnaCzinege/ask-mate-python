import bcrypt


def hash_pass(input_pass):
    hashed_bytes = bcrypt.hashpw(input_pass.encode('utf-8'), bcrypt.gensalt())
    return hashed_bytes.decode('utf-8')


def verify_pass(input_pass, hashed_pass):
    hashed_bytes_pass = hashed_pass.encode('utf-8')
    return bcrypt.checkpw(input_pass.encode('utf-8'), hashed_bytes_pass)