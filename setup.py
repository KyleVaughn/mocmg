import setuptools

setuptools.setup(
    name="mocmg",
    version="0.0",
    description="Mesh generator for solving the neutron transport equation with the method of characteristics.",
    url="http://github.com/KyleVaughn/mocmg",
    author="Kyle Vaughn",
    author_email="kcvaughn@umich.edu",
    license="MIT",
    packages=setuptools.find_packages(),
    install_requires=[
        "numpy>=1.19",
        "scipy>=1.6",
        "h5py>=3.1",
        "gmsh-dev>=4.7.1",
    ],
    include_package_data=True,
    python_requires=">=3.6",
    zip_safe=False,
)
