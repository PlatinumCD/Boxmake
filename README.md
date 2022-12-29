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
	-p py-numpy
	-p autodiff
```
or
```
boxmake create \
	--image ubuntu:22.04 \
	--name my-ubuntu-image \
	--no-spack
```
