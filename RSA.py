import random


class Person:

    def __init__(self):
        self.public_key = None
        self.private_key = None

    def encrypt(self, m):
        return pow(m, self.public_key[1]) % self.public_key[0]

    def decrypt(self, c):
        return pow(c, self.private_key[1]) % self.private_key[0]

    def decrypt_crt(self, c):
        dp, dq, qinv, p, q = self.private_key
        x1 = pow(c, dp) % p
        x2 = pow(c, dq) % q

        h = qinv * (x1-x2) % p

        return x2 + (h * q)

    def generate_keys(self, crt=False):
        # choose two prime numbers p and q
        p = random.randint(0, 50)
        while miller_rabin(p, 500) is False:
            p = random.randint(0, 50)
        q = random.randint(0, 50)
        while q != p and miller_rabin(q, 500) is False:
            q = random.randint(0, 50)
        while self.get_multiplicative_inverse(p, q, crt) is False:
            continue

    def get_multiplicative_inverse(self, p, q, crt=False):

        m_lambda = least_common_multiple(p - 1, q - 1)

        # compute an e that is coprime to m_lambda
        e = random.randint(2, m_lambda)
        # choose e such that 1 < e < m_lambda
        while m_lambda % e == 0 or miller_rabin(e, 500) is False:
            # e should be coprime -> generate primes, it shouldn't divide m_lambda
            e = random.randint(2, m_lambda)
        if e >= m_lambda:
            return False
        if int((p - q) / 2.0) == 0 or gcd(e, m_lambda) != 1:
            return False
        self.public_key = (p*q, e)
        self.private_key = (p*q, mod_inverse(e, m_lambda))

        if crt is True:
            d_p = self.private_key[1] % (p - 1)
            d_q = self.private_key[1] % (q - 1)
            q_inv = mod_inverse(q, p)
            self.private_key = (d_p, d_q, q_inv, p, q)

        return True

    def get_public_key(self):
        return self.public_key

    def receive_key(self, pub_key):
        self.public_key = pub_key


# Miller-Rabin primality test
def miller_rabin(n, k):
    if n <= 1 or n == 4:
        return False
    if n <= 3:
        return True
    # d is odd number and d*2^r is n-1
    # r > 0 is assumed since 0 < n < 1
    d = n - 1
    while d % 2 == 0:
        d /= 2.
    for i in range(k):
        if miller_test(n, d) is False:
            return False

    return True


def miller_test(n, d):
    a = random.randint(3, n-2)
    x = pow(a, d) % n

    if x == 1 or x == n-1:
        return True

    while d != n-1:
        x = (x*x) % n
        d *= 2

        if x == 1:
            return False
        if x == n-1:
            return True

    return False


# computes the greatest common denominator of two integers
def gcd(x, y):
    while y:
        x, y = y, x % y
    return x


# computes the least common multiple of two integers
def least_common_multiple(x, y):
    lcm = x*y // gcd(x, y)
    return lcm


def mod_inverse(a, m):
    a = a % m
    for x in range(1, m):
        if (a * x) % m == 1:
            return x
    return 1


if __name__ == "__main__":
    # Arlen = Person()
    # Nancy = Person()
    # Arlen.generate_keys()
    #
    # print(Arlen.public_key, Arlen.private_key)
    #
    # Nancy.receive_key(Arlen.get_public_key())
    #
    # print(Nancy.public_key, Nancy.private_key)
    #
    # M = [ord(letter) for letter in "Hello, World!"]
    # cipher = [Nancy.encrypt(m) for m in M]
    # plain_text = [Arlen.decrypt(c) for c in cipher]
    #
    # print([chr(ch) for ch in cipher])
    # pt = [chr(ch) for ch in plain_text]
    # text = ""
    # for c in pt:
    #     text += c
    # print(text)

    # Nancy.generate_keys(crt=True)
    #
    # Arlen.receive_key(Nancy.get_public_key())
    #
    # print(Nancy.public_key, Nancy.private_key)
    # print(Arlen.public_key, Arlen.private_key)
    #
    # M = [ord(letter) for letter in "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua."]
    # cipher = [Arlen.encrypt(m) for m in M]
    # plain_text = [Nancy.decrypt_crt(c) for c in cipher]
    #
    # print([chr(ch) for ch in cipher])
    # pt = [chr(int(ch)) for ch in plain_text]
    # text = ""
    # for c in pt:
    #     text += c
    # print(text)

    primes = ([miller_rabin(n, 100000) for n in range(0, 50)])

    for i in range(0, 50):
        if primes[i]:
            print(i)
