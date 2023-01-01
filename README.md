# Boxmake

Build docker images quickly with Spack integration.

### Install

```
$ pip3 install boxmake
```

### Usage

Create image

```
$ boxmake create \
	--image centos:8 \
	--name my-centos-image \
	-p py-numpy \
	-p autodiff
```
or
```
$ boxmake create \
	--image ubuntu:22.04 \
	--name my-ubuntu-image \
	--no-spack
```
or
```
$ cat test.json

{
	"image": "ubuntu:22.04",
	"name": "test-file-kokkos",
	"spack": true,
	"spack-packages": [
		"kokkos"
	],
	"os-packages": [
		"neovim"
	]
}

$ boxmake create -f test.json
```

List images

```
$ ./boxmake list

Boxmake images:
====================

	my-centos-image (centos:8): - 2022-01-01 00:00:00
		+ py-numpy
		+ autodiff

	my-ubuntu-image (ubuntu:22.04): - 2022-01-01 00:00:00
		No spack packages or spack installed

	test-file-kokkos (ubuntu:22.04): - 2022-01-01 00:00:00
		+ kokkos
```

### Examples

Create an E4S image loaded with intel oneapi compilers and create a centos:8 image loaded with kokkos in a single call:
```
$ ./boxmake create \
	--image ecpe4s/ubuntu20.04-runner-x86_64:2022-12-01 \
	--name e4s-intel \
	-p intel-oneapi-compilers \ 
&& \
./boxmake create \
	--image centos:8 \
	--name centos8-kokkos \
	-p kokkos 
```

### To do

1. Add **remove from image** feature for spack
2. Add **remove image** feature
