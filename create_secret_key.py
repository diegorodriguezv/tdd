#!/usr/bin/env python3
from django.core.management.utils import get_random_secret_key


def main():
    print(get_random_secret_key())


if __name__ == "__main__":
    main()
