from distutils.core import setup
import setuptools

setup(
    name="django-postmark-mailer",
    version=__import__("postmark_mailer").__version__,
    description="A reusable Django app for queuing the sending of email via postmarkapp.com batch messaging API",
    long_description=open("README.md").read(),
    author="Jason Emerick",
    author_email="jemerick@gmail.com",
    url="",
    packages=[
        "postmark_mailer",
        "postmark_mailer.migrations",
        "postmark_mailer.management",
        "postmark_mailer.management.commands",
    ],
    package_dir={"postmark_mailer": "postmark_mailer"},
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Framework :: Django",
    ]
)
