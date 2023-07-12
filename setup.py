from setuptools import setup
import sys

sys.argv = [__file__, "sdist", "bdist", "bdist_wheel"]  # Replace the args

print("--- 开始构建! ---")
setup(
    name="boat",
    version="0.0a1",
    packages=["boat"],
    license="MIT",
    author="chhongzh",
    description="An ast runner.",
)
print("--- 构建完成! ---")
