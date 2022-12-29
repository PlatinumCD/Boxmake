# Conex

Build docker images quickly with Spack integration.

### Install
```
pip3 install conex
```

### Usage

Create image

```
conex create \
	--image centos:8 \
	--name my-centos-image \
	-p py-numpy
	-p autodiff
```
or
```
create \
	--image ubuntu:22.04 \
	--name my-ubuntu-image \
	--no-spack
```
