# Boxmake

Build docker images quickly with Spack integration.

### Install
```
pip3 install boxmake
```

### Usage

Create image

```
boxmake create \
	--image centos:8 \
	--name my-centos-image \
	-p py-numpy \
	-p autodiff
```
or
```
boxmake create \
	--image ubuntu:22.04 \
	--name my-ubuntu-image \
	--no-spack
```

### Examples

Install intel oneapi compilers on E4S x86_64 with:
```
./boxmake create \
	--image ecpe4s/ubuntu20.04-runner-x86_64:2022-12-01 \
	--name e4s-intel \
	-p intel-oneapi-compilers
```

### To do

1. Add **Append/remove to container** feature for spack
2. Add **List boxmake images** feature that includes description of spack packages
