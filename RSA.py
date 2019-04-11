import random

"""
Do not use this script for production.
Python does not adhere to encapsulation and all variables are therefore accessible outside of class hierarchy.
This means anyone could access variable that would otherwise be private, like private keys!!!!
"""


class Person:

    def __init__(self):
        self.public_key = None
        self.e = None
        self.d = None

    def encrypt(self, m):
        return pow(m, self.e) % self.public_key

    def decrypt(self, c):
        return pow(c, self.d) % self.public_key

    def generate_keys(self):
        # choose two prime numbers p and q that are coprime
        p = random.randint(0, 100)
        while miller_rabin(p, 10) is False:
            p = random.randint(0, 100)
        q = random.randint(0, 100)
        while q != p and miller_rabin(q, 10) is False:
            q = random.randint(0, 100)
        self.public_key = p*q
        while self.get_multiplicative_inverse(p, q) is False:
            continue

    def get_multiplicative_inverse(self, p, q):
        m_lambda = least_common_multiple(p - 1, q - 1)
        e = random.randint(2, m_lambda)
        # choose e such that 1 < e < m_lambda
        while miller_rabin(e, 20) is False and m_lambda % e == 0:
            # e should be coprime -> generate primes, it shouldn't divide m_lambda
            e = random.randint(2, m_lambda)
        if e >= m_lambda:
            return False
        if gcd(e, m_lambda) != 1 or (p - q) // 2 == 0:
            return False
        self.e = e
        self.d = mod_inverse(e, m_lambda)
        return True

    def get_public_key(self):
        return self.public_key, self.e

    def receive_key(self, pub_key):
        self.public_key, self.e = pub_key


# Miller-Rabin primality test
def miller_rabin(n, k):
    if n <= 1 or n == 4:
        return False
    if n <= 3:
        return True
    # d is odd number and d*2^r is n-1
    # r > 0 is assumed since n is positive
    d = n - 1
    while d % 2 == 0:
        d /= 2.

    for i in range(k):
        if miller_test(n, d) is False:
            return False
    return True


def miller_test(n, d):
    a = random.randint(2, n-2)
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


# Don't let anyone see!!! *Remove from script before using to avoid exposing keys*
if __name__ == "__main__":
    Arlen = Person()
    Nancy = Person()
    Arlen.generate_keys()
    print(Arlen.public_key, Arlen.d, Arlen.e)
    Nancy.receive_key(Arlen.get_public_key())
    print(Nancy.public_key, Nancy.d, Nancy.e)
    cipher = Nancy.encrypt(18)
    plain_text = Arlen.decrypt(cipher)
    print(cipher)
    print(plain_text)

