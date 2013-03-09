#!/bin/sh

tar -czf naunapi.tar.gz naunapi.py naunapi.spec
rpmbuild -ta --define "_topdir $PWD/rpmbuild" naunapi.tar.gz
