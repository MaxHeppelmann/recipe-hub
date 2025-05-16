from setuptools import setup, find_packages

setup(
    name="recipe-app",
    version="0.1.0",
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        "flask>=2.0.0",
        "flask-sqlalchemy>=3.0.0",
        "psycopg2-binary>=2.9.0",
        "python-dotenv>=1.0.0",
        "gunicorn>=21.0.0",
    ],
    python_requires=">=3.7",
    
    # Add entry points to make the app callable via command
    entry_points={
        "console_scripts": [
            "recipe-app=recipe_app.main:main",
        ],
    },
    
    # Metadata for PyPI
    author="Max Heppelmann",
    author_email="heppmaxwell@gmail.com",
    description="Recipe management and sharing application",
    keywords="flask, recipe, web application",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Framework :: Flask",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
)
