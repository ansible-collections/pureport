#!/usr/bin/env bash

BASEDIR=$(dirname "$0")
mkdir -p $BASEDIR/../collections/ansible-collections/pureport
(cd  $BASEDIR/../collections/ansible-collections/pureport && ln -s ../../../../.. fabric)

